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

To produce the stats JSON file, version 5.8 (or higher) of OmegaT is necessary (soon to be released but available as of 2022-12-22 as a nightly build from the [official Github repo](https://github.com/omegat-org/omegat). 

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
python omt_check_batch_completion.py -f path/to/project_stats.json
```

or 

```
python omt_check_batch_completion.py -f path/to/project_stats.txt
```

Tested with Python 3.10.8 

## Online execution

For Github repositories: https://github.com/marketplace/actions/omegat-stat. It might be possible to implement a similar routine in AWS CodeCommit or Azure DevOps.

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

## Example using a virtual environment

### Fetch OmegaT project

```bash
# set omegat project name
omt_proj="project_cycle-stage_xx-YY_step"

# clone project's repo
git clone https://git-codecommit.eu-central-1.amazonaws.com/v1/repos/$omt_proj

# get absolute path of the clone project's folder
omt_proj_path=$(readlink -f $omt_proj)

# use omegat to obtain project stats in json
java -jar /home/souto/Repos/omegat-org/omegat/build/install/OmegaT/OmegaT.jar $omt_proj_path  --mode=console-stats --output-file=$omt_proj_path/omegat/project_stats.json
```

### Set up application

```bash
# clone app's repo
gh repo clone capstanlqc/check-batch-completion

# get absolute path to the app's root directory
app_root=$(readlink -f check-batch-completion)

# change directory to the app's root directory
cd $app_root
```

You may create a virtual environment and install dependencies using _either_ poetry:

```bash
# install dependencies with poetry
poetry install
```

_or_ a more standard approach (with more steps) using pip and venv:

```bash
# create virtual environment
python -m venv venv

# install dependencies with pip (activating the virtual environment)
source venv/bin/activate && pip install -r requirements.txt && deactivate
```

### Run the application

Depending on your choice above, you may run the application using _either_ poetry:

```bash
# run app with poetry
cd $app_root && poetry run python omt_check_batch_completion.py -f $omt_proj_path/omegat/project_stats.json && cd -
```

_or_ venv: 

```bash
source $app_root/venv/bin/activate && python $app_root/omt_check_batch_completion.py -f $proj_path/omegat/project_stats.json && deactivate
```