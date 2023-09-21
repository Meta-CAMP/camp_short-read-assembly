# Short-Read Assembly

[![Documentation Status](https://img.shields.io/readthedocs/camp_short-read-assembly)](https://camp-documentation.readthedocs.io/en/latest/short-read-assembly.html) ![Version](https://img.shields.io/badge/version-0.5.0-brightgreen)

## Overview

This module is designed to function as both a standalone short-read assembly pipeline as well as a component of the larger CAMP metagenome analysis pipeline. As such, it is both self-contained (ex. instructions included for the setup of a versioned environment, etc.), and seamlessly compatible with other CAMP modules (ex. ingests and spawns standardized input/output config files, etc.). 

Both MetaSPAdes and MegaHit are provided as assembly algorithm options. 

## Approach

Under construction.

## Installation

1. Clone repo from [Github](<https://github.com/MetaSUB-CAMP/camp_short-read-assembly>).
```Bash
git clone https://github.com/MetaSUB-CAMP/camp_short-read-assembly
```

2. Set up the conda environment using `configs/conda/short-read-assembly.yaml`. 
```Bash
# Create and activate conda environment 
cd camp_short-read-assembly
conda env create -f configs/conda/short-read-assembly.yaml
conda activate short-read-assembly
```

3. Update the relevant parameters i.e.: choice and mode (metagenomics, metaviral, etc.) of assembler in `test_data/parameters.yaml`.

4. Make sure the installed pipeline works correctly. With 40 threads and a maximum of 50 GB allocated, the test dataset should finish in approximately 2 minutes.
```Bash
# Run tests on the included sample dataset
python /path/to/camp_short-read-assembly/workflow/short-read-assembly.py test
```

## Using the Module

**Input**: `/path/to/samples.csv` provided by the user.

**Output**: 1) An output config file summarizing 2) the module's outputs, which are assembled contigs. 

- `/path/to/work/dir/short-read-assembly/final_reports/samples.csv` for ingestion by the next module

- `/path/to/work/dir/short-read-assembly/final_reports/sample_name.metaspades.fasta` and/or `sample_name.megahit.fasta`, which are the outputs of MetaSPAdes and MegaHit respectively

**Structure**:
```
└── workflow
    ├── Snakefile
    ├── short-read-assembly.py
    ├── utils.py
    └── __init__.py
```
- `workflow/short-read-assembly.py`: Click-based CLI that wraps the `snakemake` and other commands for clean management of parameters, resources, and environment variables.
- `workflow/Snakefile`: The `snakemake` pipeline. 
- `workflow/utils.py`: Sample ingestion and work directory setup functions, and other utility functions used in the pipeline and the CLI.

### Running the Workflow

1. Make your own `samples.csv` based on the template in `configs/samples.csv`. Sample test data can be found in `test_data/`. 
    - `ingest_samples` in `workflow/utils.py` expects Illumina reads in FastQ (may be gzipped) form and de novo assembled contigs in FastA form
    - `samples.csv` requires either absolute paths or paths relative to the directory that the module is being run in

2. Update the relevant parameters in `configs/parameters.yaml`.

3. Update the computational resources available to the pipeline in `configs/resources.yaml`. 

#### Command Line Deployment

To run CAMP on the command line, use the following, where `/path/to/work/dir` is replaced with the absolute path of your chosen working directory, and `/path/to/samples.csv` is replaced with your copy of `samples.csv`. 
    - The default number of cores available to Snakemake is 1 which is enough for test data, but should probably be adjusted to 10+ for a real dataset.
    - Relative or absolute paths to the Snakefile and/or the working directory (if you're running elsewhere) are accepted!
    - The parameters and resource config YAMLs can also be customized.
```Bash
python /path/to/camp_short-read-assembly/workflow/short-read-assembly.py \
    (-c number_of_cores_allocated) \
    (-p /path/to/parameters.yaml) \
    (-r /path/to/resources.yaml) \
    -d /path/to/work/dir \
    -s /path/to/samples.csv
```

#### Slurm Cluster Deployment

To run CAMP on a job submission cluster (for now, only Slurm is supported), use the following.
    - `--slurm` is an optional flag that submits all rules in the Snakemake pipeline as `sbatch` jobs. 
    - In Slurm mode, the `-c` flag refers to the maximum number of `sbatch` jobs submitted in parallel, **not** the pool of cores available to run the jobs. Each job will request the number of cores specified by threads in `configs/resources/slurm.yaml`.
```Bash
sbatch -J jobname -o jobname.log << "EOF"
#!/bin/bash
python /path/to/camp_short-read-assembly/workflow/short-read-assembly.py --slurm \
    (-c max_number_of_parallel_jobs_submitted) \
    (-p /path/to/parameters.yaml) \
    (-r /path/to/resources.yaml) \
    -d /path/to/work/dir \
    -s /path/to/samples.csv
EOF
```

#### Finishing Up

1. To plot grouped bar graph(s) of the number of reads and bases in each *de novo* assembly (from each sample), set up the dataviz environment and follow the instructions in the Jupyter notebook:
```Bash
conda env create -f configs/conda/dataviz.yaml
conda activate dataviz
jupyter notebook &
```

2. After checking over `final_reports/` and making sure you have everything you need, you can delete all intermediate files to save space. 
```Bash
python3 /path/to/camp_short-read-assembly/workflow/short-read-assembly.py cleanup \
    -d /path/to/work/dir \
    -s /path/to/samples.csv
```

3. If for some reason the module keeps failing, CAMP can print a script containing all of the remaining commands that can be run manually. 
```Bash
python3 /path/to/camp_short-read-assembly/workflow/short-read-assembly.py --dry_run \
    -d /path/to/work/dir \
    -s /path/to/samples.csv
```

## Credits

- This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter>) as a simplified version of the [project template](https://github.com/audreyr/cookiecutter-pypackage>).
- Free software: MIT
- Documentation: https://camp-documentation.readthedocs.io/en/latest/short-read-assembly.html
