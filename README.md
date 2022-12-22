# Check batch completion in OmegaT project

This script will check a statistics file issued from an OmegaT project and will report whether each batch is complete or not. 

## Definitions

| Term     | Definition | 
|:---------|:----------|
| Batch    | Folder inside the `source` folder containing translation files. |
| Complete | All segments in all files belong to a batch are translated.     |

## Preconditions

### 1. Source folder structure

This script assumes that the `source` folder of the project has the following 2-level structure (where the first level has the batch folders and the second level has the files themselves):

```
source > tree .
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
``` 

### 2. Statistics file 

The script expects either a regular OmegaT statistics text file (`project_stats.txt`) or a new statistics JSON file (`project_stats.json`).

The stats text file is generated whenever the OmegaT project is open in OmegaT, or by running OmegaT on the command line on the project, like so:

```
java -jar /path/to/OmegaT_5.7.1/OmegaT.jar /path/to/project --mode=console-translate
``` 

To produce the stats JSON file, version 5.8 (or higher) of OmegaT is necessary (soon to be released but available as of 2022-12-22 as a nightly build from the [official Github repo](github.com/).omegat-org/omegat). 

```
java -jar /path/to/OmegaT_5.8.0/OmegaT.jar /path/to/project --mode=console-stats --output-file=project_stats.json
``` 

Run the following command to see other related options:

```
java -jar /path/to/OmegaT_5.8.0/OmegaT.jar --help
```

## Offline execution

Call the script as:

```
python omt_check_batch_completion.py -f /path/to/project_stats.json
```

or 

```
python omt_check_batch_completion.py -f /path/to/project_stats.txt
```

Tested with Python 3.10.8 

## Online execution

For Github repositories: https://github.com/marketplace/actions/omegat-stat

## Results

Results are returned in the form of a dictionary where the key is tha name of the batch and the value is the completion status.

```python
{
  'batch1': False, 
  'batch2': True, 
  'batch3': False
}
``` 

Batches that are completed (e.g. batch2 above) can be pushed to the next step in the workflow.

