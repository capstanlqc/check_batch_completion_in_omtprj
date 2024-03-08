#!/usr/bin/env python3

# generate stats from OmegaT as
# java -jar /path/to/5.8//OmegaT.jar --mode=console-stats /path/to/proj --output-file=project_stats.json

# call the script as
# python3.10 omt_check_batch_completion.py -f /path/to/project_stats.json
# or 
# python3.10 omt_check_batch_completion.py -f /path/to/project_stats.txt

'''
this script assumes that the source folder has the following 2-level structure
where the first level is the batch folders and the second level the files themselves:

source  tree .
.
├── batch01
│   ├── file1.xml
│   └── file2.xml
├── batch02
│   ├── file3.xml
│   ├── file4.xml
│   └── file5.xml
└── batch3
    ├── file6.xml
    └── file7.xml
''' 

### imports 

import sys, os, re
import pandas as pd
import json
import argparse
from functools import reduce

### functions

def get_batch_status_from_json(fpath, regex):
    """ 
    Takes a json stats file produced with OmegaT 5.8 / 6.0 --mode=console-stats and
    creates a dictionary with completed status for each batch.
    """ 

    # open file and return JSON object as a data dictionary
    with open(fpath, 'r') as f:
        data = json.load(f)

    # iterate through the data
    for file in data["files"]:
        fpath = file["filename"].strip()
        
        if regex.match(fpath):
            # get folder (batch) name from the file path
            batch_name = fpath.split("/")[0] 
            if batch_name in completed and completed[batch_name] == False:
                # if one file was incomplete in the batch, 
                # no need to check other files in the same batch
                continue

            remaining = file["remaining"]["segments"]
            if int(remaining) == 0:
                completed.update({batch_name: True})
            else:
                completed.update({batch_name: False})

    return completed


def get_batch_status_from_text(fpath, regex):
    """ 
    Takes a text stats file produced with OmegaT (any version) and
    creates a dictionary with completed status for each batch.
    """ 

    # open file and return list of lines
    with open(fpath, 'r') as f:
        lines = f.readlines()

    # iterate through the data 
    for line in lines:

        if regex.match(line):
            # get folder (batch) name from the file path
            batch_name = line.strip().split()[0].split("/")[0]
            if batch_name in completed and completed[batch_name] == False:
                # if one file was incomplete in the batch, 
                # no need to check other files in the same batch
                continue

            # third column, with "Remaining Segments" header
            remaining = line.strip().split()[2]
            if int(remaining) == 0:
                completed.update({batch_name: True})
            else:
                completed.update({batch_name: False})

    return completed


### logic 
if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='omt_check_batch_completion', description='Check batch completion based on the (already existing) project_stats.json or project_stats.txt files')
    parser.add_argument('-f', '--filename', help='Path to stats file (either json or txt). Required.')
    parser.add_argument('-b', '--batch', help='Batch to check for completion. If not defined it looks for all batches/remaining segments')
    parser.add_argument('-s', '--single', help='Returns a single value/string only, a True or a False', action="store_true")
    args = parser.parse_args()

    if not args.filename or not os.path.isfile(args.filename):
        parser.print_help(sys.stderr)
        sys.stderr.write(f'\nERROR: filename "{args.filename}" is not defined or not a file!\n')
        sys.exit(1)

    ### constants
    completed = {}
    if args.batch:
        batch_name_pattern = r"^" + re.escape(args.batch) + r"/"
    else:
        # We  create a batch looking regex so the project_stats.txt file is also properly parsed
        batch_name_pattern = r"^[0-9]{2}_[-_A-Z]+/"
    regex = re.compile(batch_name_pattern, re.IGNORECASE)

    if args.filename.lower().endswith(('.json')):
        completed = get_batch_status_from_json(args.filename, regex)
    elif args.filename.lower().endswith(('.txt')):
        completed = get_batch_status_from_text(args.filename, regex)

    # print results
    if not args.single:
        for k, v in completed.items():
            print(f"batch '{k}' complete? {v}")
    elif args.batch:
        print("True" if completed.get(args.batch, False) else "False")
    else:
        print(reduce(lambda a, b: a and b, completed.values(), True))
    

