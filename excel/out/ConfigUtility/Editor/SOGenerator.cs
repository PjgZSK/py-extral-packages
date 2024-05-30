using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEngine;

public static class SOGenerator
{
    private static Dictionary<string, SOPersistentData> _pathDataDic = null;
    private static Dictionary<string, SOPersistentData> PathDataDic
    {
        get
        {
            if (_pathDataDic == null)
            {
                if (!File.Exists(SODirConfig.persistentDataUnityPath))
                {
                    _pathDataDic = new Dictionary<string, SOPersistentData>();
                }
                else
                {
                    using (StreamReader sr = new StreamReader(SODirConfig.persistentDataUnityPath))
                    {
                        _pathDataDic = JsonConvert.DeserializeObject<Dictionary<string, SOPersistentData>>(sr.ReadToEnd());
                    }
                }
            }
            return _pathDataDic;
        }
    }

    [MenuItem("SOGenerator/UpdateSO")]
    public static void GenSOOnDemand()
    {
        var jsonFiles = Directory.GetFiles(SODirConfig.jsonUnityDir, "*.json");
        List<string> excludeJsonFiles = new List<string>();
        foreach (var f in jsonFiles)
        {
            var ff = f.Replace(@"\", @"/");
            if (PathDataDic.ContainsKey(ff) && PathDataDic[ff].lastGenerationTime > File.GetLastWriteTimeUtc(f).Ticks)
            {
                excludeJsonFiles.Add(ff);
            }
        }
        Debug.Log($"Exclude files: {string.Join(",", excludeJsonFiles)}");

        GenSO(excludeJsonFiles);
    }

    [MenuItem("SOGenerator/GenAllSO")]
    public static void GenAllSO()
    {
        GenSO();
    }

    private static void GenSO(List<string> excludeJsonFile = null)
    {
        bool changed = false;
        Assembly asm = Assembly.Load("Assembly-CSharp");
        foreach (var t in asm.GetTypes())
        {
            var a = t.GetCustomAttribute<SOGenConfigAttribute>(true);
            if (a == null)
            {
                continue;
            }
            if (excludeJsonFile != null && excludeJsonFile.Contains(a.jsonUnityPath))
            {
                continue;
            }
            GenSO(a.jsonUnityPath, a.soInstanceUnityPath, a.dataType, t);
            Debug.Log($"Generate so using {a.jsonUnityPath}");

            PathDataDic[a.jsonUnityPath] = new SOPersistentData
            {
                lastGenerationTime = DateTime.UtcNow.Ticks,
                path = a.jsonUnityPath
            };
            changed = true;
        }

        if (changed == true)
        {
            using (StreamWriter sw = new StreamWriter(SODirConfig.persistentDataUnityPath))
            {
                sw.Write(JsonConvert.SerializeObject(PathDataDic));
            }
        }
    }

    private static void GenSO(string jsonPath, string soPath, Type dataType, Type soType)
    {
        var t = typeof(List<>).MakeGenericType(dataType);
        object data = null;
        using (StreamReader sr = new StreamReader(jsonPath))
        {
            var setting = new JsonSerializerSettings();
            setting.NullValueHandling = NullValueHandling.Ignore;
            data = JsonConvert.DeserializeObject(sr.ReadToEnd(), t, setting);
        }

        foreach (var a in (IEnumerable)data)
        {
            var md = dataType.GetMethod("ProcessUnityAssets", BindingFlags.NonPublic | BindingFlags.Instance);
            md.Invoke(a, null);
        }

        UnityEngine.Object so;
        if (File.Exists(soPath))
        {
            so = AssetDatabase.LoadMainAssetAtPath(soPath);
        }
        else
        {
            so = ScriptableObject.CreateInstance(soType);
            AssetDatabase.CreateAsset(so, soPath);
            AssetDatabase.SaveAssets();
        }
        var f = soType.GetField("_data");
        f.SetValue(so, data);

        EditorUtility.SetDirty(so);
    }

    private static void GenSO<DataT, SoT>(string jsonPath, string soPath) where SoT : SOBase<DataT>
    {
        GenSO(jsonPath, soPath, typeof(DataT), typeof(SoT));
    }

}
