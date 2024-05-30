from sys import path
from pathlib import Path
cur_path = Path(__file__)
path.append(cur_path.parent.parent.as_posix())

import os
from pathlib import Path
import argparse
import jsontree

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs=None,
                        help='a directory path with -j/default or a JSON file with -t',)
    parser.add_argument('-o', '--out', default='out',
                        help='output directory')
    parser.add_argument('-name', '--jsonname', default='a.json',
                        help='a string for output JSON file name')
    parser.add_argument('-i', '--ignore', default=None, 
                        help='a re pattern to match files which will be ignored at \
                            convertin a direction into a JSON file')
    parser.add_argument('-c', '--content', action='store_true',
                        help='will store file content')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-j', '--json', action='store_true', 
                       help='convert a directory path into a JSON file')
    group.add_argument('-t', '--tree', action='store_true', 
                       help='create a directory using a JSON file')
    options = parser.parse_args()

    out_path = Path(options.out)
    if (out_path.exists() == False):
        os.makedirs(options.out, exist_ok=True)

    if (options.tree):
        jsontree.create_tree(open(options.infile), options.out)
    else: 
        json_path = os.path.join(options.out, options.jsonname)
        if (options.json):
            jsontree.create_json(options.infile, open(json_path, 'w'), options.ignore, options.content)
        else:
            jsontree.create_json(options.infile, open(json_path, 'w'), options.ignore, options.content)
            jsontree.create_tree(open(json_path), options.out)

if __name__ == '__main__':
    main()