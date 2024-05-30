__version__ = '0.1.0'
__all__ = [
    'create_trees', 'create_tree',
    'create_jsons', 'create_json',
]

__author__ = 'pengjungang'

from .tree import directory_to_jsons
from .tree import directory_to_json
from .tree import json_to_directorys
from .tree import json_to_directory

def create_trees(s, path):
    """create directory tree at ``path`` using ``s`` (a JSON ``str``)"""
    return json_to_directorys(s, path)

def create_tree(fp, path):
    """create directory tree at ``path`` using ``fp`` (a file-like object supporting ``.read()`` operation)"""
    return json_to_directory(fp, path)

def create_jsons(path, ignore, read_content: bool = False):
    """create a JSON ``str`` which describes directory tree at ``path``, ``ignore`` is a re pattern ``str`` for 
    filtering file and dir
    """
    return directory_to_jsons(path, ignore, read_content) 

def create_json(path, fp, ignore, read_content: bool = False):
    """create a JSON file using ``fp``(a file-like object supporting ``.write()`` operation) which
       describes directory tree at ``path``, ``ignore`` is a re pattern ``str`` for filtering file 
       and dir
    """
    directory_to_json(path, fp, ignore, read_content)