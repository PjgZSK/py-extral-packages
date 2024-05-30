import os
import re

class TreeNode:
    def __init__(self) -> None:
        """type 0:file, 1:directory"""
        self.name = "" 
        self.path = ""
        self.type = 0 
        self.parent = None
        self.childern = []
        self.content = "" 

def json_dict(t):
    if (isinstance(t, TreeNode) == False):
        return t

    dct = {}
    for k,v in t.__dict__.items():
        if (k == 'parent'):
            dct['parent'] = None if v == None else v.name
        else:
            dct[k] = v
    return dct


def create_dir(node: TreeNode, path: str):
        """create a dir, return root path"""
        p = os.path.join(path, node.name)
        if (node.type == 0):
            with open(p, 'w') as f:
                f.write(node.content)
        elif (node.type == 1):
            os.makedirs(name= p, exist_ok= True)
            for c in node.childern:
                create_dir(c, os.path.join(path, node.name))
        return p

def travel_directory(path: str, ignore: str, read_content: bool, relative_path: str) -> TreeNode:
    root = TreeNode()
    root.type = 1
    root.name = os.path.basename(path)
    root.path = relative_path + '/' + root.name if relative_path != '' else root.name

    entries = os.scandir(path)
    for entry in entries:
        if (ignore != None and \
            re.match(ignore, entry.name) != None):
            continue 
        if (entry.is_dir()):
            d = travel_directory(entry.path, ignore, read_content, root.path)
            d.parent = root 
            root.childern.append(d)
        elif (entry.is_file()):
            node = TreeNode()
            node.name = entry.name
            node.path = root.path + '/' + node.name
            node.type = 0 
            node.parent = root
            if (read_content):
                with open(entry.path) as f:
                    node.content = f.read()
            root.childern.append(node)
    return root

def directory_to_tree(path, ignore = None, read_content: bool = False):
    if (os.path.isdir(path) == False):
        raise Exception("not dir")
    tree = travel_directory(path, ignore, read_content, '')
    return tree

def as_tree_node(dct):
        node = TreeNode()
        for k,v in dct.items():
            if (k == 'childern'):
                for l in v:
                    if (isinstance(l, TreeNode)):
                        node.childern.append(l)
            elif (k == 'name'):
                node.name = v
            elif (k == 'type'):
                node.type = v
            elif (k == 'content'):
                node.content = v 
            elif (k == 'parent'):
                node.parent = v
        return node