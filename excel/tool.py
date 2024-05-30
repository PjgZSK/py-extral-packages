"""
1.
    copy unity configutility to your unity project
    Usage:
        cp -r out/configutility your/unity/project
    
    Example:
        cp -r out/configutility /e/UnityProject/My\ project/Assets/
2.
    generate so files which contains so csharp file, so data csharp file and json fils
    Usage:
        python tool.py absolute/tree/path relative/unity/tree/path xl/file/path

    Example:
        python tool.py E:\\UnityProject\\My\ Project\\Assets Assets test.xlsx
        python tool.py /e/UnityProject/My\ Project/Assets Assets test.xlsx
"""
from sys import path
from pathlib import Path
cur_path = Path(__file__)
path.append(cur_path.parent.parent.as_posix())

from argparse import ArgumentParser
from excel.unityextend.unityso import UnitySO
from excel.jsonexcel.jexcel import excel_to_json

def main():
    parser = ArgumentParser()
    parser.add_argument('tree', 
                        help='''The absolute path to ConfigUtility's parent''')
    parser.add_argument('utree', default='Assets',
                        help='The relative path to unity project')
    parser.add_argument('xl', 
                        help='xl file path to generate config files')
    options = parser.parse_args()    

    print(options.tree)
    so = UnitySO(options.tree, options.utree)
    dic = excel_to_json(options.xl, so._json_dir())
    for name, attrs in dic.items():
        so.generate_so_files(name, attrs)

if __name__ == '__main__':
    main()

