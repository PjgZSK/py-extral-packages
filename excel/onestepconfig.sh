python jsontree/tool.py /e/UnityProject/FIFA2024/Assets/Tools/ConfigUtility -o out -name configutility.json -i .*\.meta$ -c

cp out/configutility.json unityextend/config/
cp out/configutility/Runtime/Data/__ConfigTestType.cs unityextend/config/
cp out/configutility/Runtime/SO/__SOTemplate.cs unityextend/config/
cp out/configutility/Editor/SODirConfig.cs unityextend/config/

rm out/configutility/Runtime/Data/__ConfigTestType.cs 
rm out/configutility/Runtime/SO/__SOTemplate.cs 