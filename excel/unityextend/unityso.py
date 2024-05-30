"""
Creating a directory tree(contains unity c# code and JSON file) that can used by unity 
directly to generate scriptobject instance according to json file.
This directory tree is created by a special JSON file.

After this directory tree is created, for generating a new scriptobject instance,
we need create a JSON file, a c# data class file and a c# custom scriptobject class file, 
then copy them to specific path in this directory tree . 

The directory tree's structure is as below:
configutility
├── Editor
│   ├── Jsons
│   ├── PersistentData
│   │   └── SOPersistentData.cs
│   ├── SODirConfig.cs
│   └── SOGenerator.cs
└── Runtime
    ├── Data
    │   └── __ConfigTestType.cs
    ├── Resources
    │   └── Configs
    ├── SO
    │   └── __SOTemplate.cs
    ├── SOBase.cs
    └── SOGenConfigAttribute.cs

Generated JSON files path:                          configutility/Editor/Jsons/
Unity c# data class files path:                     configutility/Runtime/Data/
Unity c# custom scriptobject class files path:      configutility/Runtime/SO/
Config file for this directory tree:                configutility/Editor/SODirConfig.cs
"""

from ..jsontree import create_tree
from .unitysopath import UnitySOPath
from .unitysopath import UnitySOConfigPath

class UnitySO(UnitySOPath):
    _TYPE = {
        int : '\tpublic int __name__;\n',
        float : '\tpublic float __name__;\n',
        str : '\tpublic string __name__;\n',
        bool : '\tpublic bool __name__;\n',
    }
    _SPTYPE = {
        'Material': '\tpublic Material __name__;\n',
        'Sprite': '\tpublic Sprite __name__;\n',
    }

    def generate_directory_tree(self):
        """generate directory trees and return path list"""
        return create_tree(open(UnitySOConfigPath._tree_json), self._tree_root)

    def generate_config(self, path = None):
        """generate directory tree config file and return path"""
        with open(UnitySOConfigPath._config_template) as fr:
            s = fr.read()
            path = path if path != None else self._config_path()
            with open(path, 'w') as f:
                s = s.replace('$jsonUnityDir$', self._json_unity_dir())
                s = s.replace('$persistentDataUnityPath$', self._persistent_unity_path())
                f.write(s) 
                return path

    def generate_so_files(self, base_name: str, a_t: dict, so_path = None, data_path = None):
        """generate so class file and so data type class file and return so_path and data_path"""
        so_name = base_name + 'ScriptableObject'
        data_name = base_name + 'DataType'
        so_path = so_path if so_path != None else self._so_path(so_name) 
        data_path = data_path if data_path != None else self._data_path(data_name)

        with open(UnitySOConfigPath._so_template) as so_fr:
            so_s = so_fr.read()
            with open(so_path, 'w') as so_fw:
                so_s = self._replace_so(base_name, so_name, data_name, so_s)
                so_fw.write(so_s)
        
        with open(UnitySOConfigPath._data_template) as data_fr:
            data_s = data_fr.read()
            with open(data_path, 'w') as data_fw:
                data_s = self._replace_data(a_t, data_name, data_s)
                data_fw.write(data_s)
        return [so_path, data_path]

       
    def _replace_data(self, a_t, data_name, data_s):
        filed_s = ''
        process_s = ''
        for attr,t in a_t.items():
            try:
                filed_s += self._TYPE[t].replace('__name__', str(attr)) 
                if (t == str):
                    filed_s, process_s = self._add_process(filed_s, process_s, attr)
            except KeyError:
                print(f'{t} is not supported')
        data_s = data_s.replace('//$Field_S$//', filed_s)
        data_s = data_s.replace('//$Process_S$//', process_s)
        data_s = data_s.replace('__ConfigTestType', data_name)
        return data_s

    def _replace_so(self, type_name, so_name, data_name, so_s):
        so_s = so_s.replace('__SOTemplate', so_name)
        so_s = so_s.replace('__ConfigTestType', data_name)
        so_s = so_s.replace('$jsonUnityPath$', self._json_unity_path(type_name))
        so_s = so_s.replace('$soInstanceUnityPath$', self._soins_untiy_path(so_name))
        return so_s

    def _add_process(self, filed_s, process_s, attr):
        for t,s in self._SPTYPE.items():
            if (attr.endswith(t)):
                sp_name = attr.removesuffix(t)
                filed_s += s.replace('__name__', sp_name)
                process_s += self._get_process_s(attr, t, sp_name)
                break
        return [filed_s, process_s]

    def _get_process_s(self, attr, t, sp_name):
        process_ts = '\t\t__spname__ = AssetDatabase.LoadAssetAtPath<__sptype__>(__sppath__);'
        process_ts = process_ts.replace('__spname__', sp_name)
        process_ts = process_ts.replace('__sptype__', t)
        process_ts = process_ts.replace('__sppath__', attr)
        return process_ts

