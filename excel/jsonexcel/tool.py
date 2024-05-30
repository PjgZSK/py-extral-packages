from sys import path
from pathlib import Path
cur_path = Path(__file__)
path.append(cur_path.parent.parent.as_posix())

import argparse
from jsonexcel import json_to_excel
from jsonexcel import excel_to_json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', 
                        help='excel file path or json file path')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-j', '--json', action='store_true',
                       help='convert an excel file into a JSON file')
    group.add_argument('-e', '--excel', action='store_true',
                       help='convert a JSON file into an excel file')
    options = parser.parse_args()

    if options.json:
        excel_to_json(options.infile)
    elif options.excel:
        json_to_excel([options.infile], 'temp.xlsx')

if __name__ == '__main__':
    main()