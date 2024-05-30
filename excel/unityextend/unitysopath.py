from os.path import dirname
from os.path import join
from pathlib import Path

class UnitySOConfigPath:
    _dir = dirname(__file__) + '/'
    _tree_json = _dir + 'config/configutility.json'
    _config_template = _dir + 'config/SODirConfig.cs' 
    _data_template = _dir + 'config/__ConfigTestType.cs'
    _so_template = _dir + 'config/__SOTemplate.cs'
    
class UnitySOPath:
    _rlv_json_dir = 'Editor/Jsons'
    _rlv_config_path = 'Editor/SODirConfig.cs'
    _rlv_data_dir = 'Runtime/Data'
    _rlv_so_dir = 'Runtime/SO'
    _rlv_soins_dir = 'Runtime/Resources/Configs'
    _rlv_persistent_path = 'Editor/PersistentData/genrecord.json'
    
    def __init__(self, tree_root: str, unity_root: str) -> None:
        """
        create a dirctory tree, a config file, and so files
        ``tree_path`` is where the directory tree is 
        ``root_path`` is relative path to unity project
        """
        self._tree_root = tree_root 
        self._root = join(tree_root, 'ConfigUtility')
        self._unity_root = join(unity_root, 'ConfigUtility')

    def _config_path(self):
        return join(self._root, self._rlv_config_path)

    def _persistent_unity_path(self):
        return Path(join(self._unity_root, self._rlv_persistent_path)).as_posix()

    def _data_dir(self):
        return join(self._root, self._rlv_data_dir)
    
    def _data_path(self, data_name):
        return join(self._data_dir(), data_name + '.cs')

    def _data_unity_dir(self):
        return Path(join(self._unity_root, self._rlv_data_dir)).as_posix()
    
    def _data_unity_path(self, data_name):
        return Path(join(self._data_unity_dir(), data_name + '.cs')).as_posix()

    def _so_dir(self):
        return join(self._root, self._rlv_so_dir)
     
    def _so_path(self, so_name):
        return join(self._so_dir(), so_name + '.cs')

    def _soins_unity_dir(self):
        return Path(join(self._unity_root, self._rlv_soins_dir)).as_posix()
     
    def _soins_untiy_path(self, so_name):
        return Path(join(self._soins_unity_dir(), so_name + '.asset')).as_posix()

    def _json_unity_dir(self):
        return Path(join(self._unity_root, self._rlv_json_dir)).as_posix()

    def _json_unity_path(self, type_name):
        return Path(join(self._json_unity_dir(),  type_name + '.json')).as_posix()

    def _json_dir(self):
        return join(self._root, self._rlv_json_dir)

    def _json_path(self, type_name):
        return join(self._json_dir(),  type_name + '.json')