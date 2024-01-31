#!/usr/bin/env python3

# generate stats from OmegaT as
# java -jar /path/to/5.8//OmegaT.jar --mode=console-stats /path/to/proj --output-file=project_stats.json

# call the script as
# python3.10 omt_check_batch_completion.py -f /path/to/project_stats.json -b 03_COS_SCI-C_N
# or 
# python3.10 omt_check_batch_completion.py -f /path/to/project_stats.txt -b 03_COS_SCI-C_N

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


# argument after -f 
fpath = sys.argv[2]
# argument after -b 
batch = sys.argv[4]

### constants

completed = {}
# fpath = "project_stats.txt"
# fpath = "output.json"
# batch_name_pattern = r"^(batch\d+)/"
batch_name_pattern = r"^" + re.escape(batch) + r"/"
regex = re.compile(batch_name_pattern, re.IGNORECASE)


### logic 

if __name__ == "__main__":

    if not os.path.isfile(fpath):
        print("File not found.")
        sys.exit(0)

    if fpath.lower().endswith(('.json')):
        completed = get_batch_status_from_json(fpath, regex)
    elif fpath.lower().endswith(('.txt')):
        completed = get_batch_status_from_text(fpath, regex)

    # print results
    #for k, v in completed.items():
    #    print(f"batch '{k}' complete? {v}")
    # Also return false when the batch is not found
    print("True" if completed.get(batch,False) else "False"
