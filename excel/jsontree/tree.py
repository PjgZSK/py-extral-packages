import json
from .tnode import directory_to_tree 
from .tnode import create_dir
from .tnode import as_tree_node
from .tnode import json_dict 

def directory_to_json(dir, fp, ignore = None, read_content: bool = False):
    fp.write(directory_to_jsons(dir, ignore, read_content))

def directory_to_jsons(dir, ignore = None, read_content: bool = False):
    tree = directory_to_tree(dir, ignore, read_content) 
    return json.dumps(tree, indent=4, default=lambda o:json_dict(o))

def json_to_directory(fp, dir: str):
    return json_to_directorys(fp.read(), dir)

def json_to_directorys(s, dir):
    """generate directory according to json file"""
    """a json object represent a tree node which describes a file or directory"""
    """a json array represent a list of tree node"""
    tree = json.loads(s, object_hook=as_tree_node)
    paths = []
    if (isinstance(tree, list)):
        for l in tree:
            paths.append(create_dir(l, dir))
    else:
        paths.append(create_dir(tree, dir))
    return paths

