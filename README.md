# CAMP: Short-Read Assembly

Overview
--------

This module is designed to function as both a standalone MAG short-read assembly pipeline as well as a component of the larger CAMP/CAP2 metagenome analysis pipeline. As such, it is both self-contained (ex. instructions included for the setup of a versioned environment, etc.), and seamlessly compatible with other CAMP modules (ex. ingests and spawns standardized input/output config files, etc.). 

Both MetaSPAdes and MegaHit are provided as assembly algorithm options. 

Approach
--------
<INSERT PIPELINE IMAGE>

Installation
------------

1. Clone repo: 

```
git clone <https://github.com/MetaSUB-CAMP/camp_short-read-assembly>
```

2. Set up the conda environment using ``configs/conda/short-read-assembly.yaml``. 

```
cd camp_short-read-assembly
conda env create -f configs/conda/short-read-assembly.yaml
conda activate short-read-assembly
```

3. Make sure the installed pipeline works correctly. ``pytest`` only generates temporary outputs so no files should be created.

```
pytest .tests/unit/
```

Quickstart
----------

Running each CAMP module takes the same three steps, listed below.

1. As with all CAMP modules, update the parameters.yaml file:

<TABLE OF PARAMETERS AND DESCRIPTIONS>

2. Generate your samples.csv file in the following format:

<SAMPLES.CSV FORMAT>

3. Deploy!

<SNAKEMAKE COMMAND>

Module details
---------------

**Input**: ``/path/to/samples.csv`` provided by the user.

**Output**: 1) An output config file summarizing 2) the module's outputs, which are assembled contigs. 

- ``/path/to/work/dir/short-read-assembly/final_reports/samples.csv`` for ingestion by the next module

- ``/path/to/work/dir/short-read-assembly/final_reports/metaspades.scaffolds.fasta`` and/or ``megahit.contigs.fasta``, which are the outputs of MetaSPAdes and MegaHit respectively

**Structure**:
```
└── workflow
    ├── Snakefile
    ├── short-read-assembly.py
    ├── utils.py
    └── __init__.py
```
* ``workflow/short-read-assembly.py``: Click-based CLI that wraps the ``snakemake`` and unit test generation commands for clean management of parameters, resources, and environment variables.
* ``workflow/Snakefile``: The ``snakemake`` pipeline. 
* ``workflow/utils.py``: Sample ingestion and work directory setup functions, and other utility functions used in the pipeline and the CLI.

1. Make your own ``samples.csv`` based on the template in ``configs/samples.csv``. Sample test data can be found in ``test_data/``. 
    - ``ingest_samples`` in ``workflow/utils.py`` expects Illumina reads in FastQ (may be gzipped) form and de novo assembled contigs in FastA form
    - ``samples.csv`` requires either absolute paths or paths relative to the directory that the module is being run in

2. Update the relevant parameters in ``configs/parameters.yaml``.

3. Update the computational resources available to the pipeline in ``resources.yaml``. 


Command line deployment
-----------------------
To run CAMP on the command line, use the following, where ``/path/to/work/dir`` is replaced with the absolute path of your chosen working directory, and ``/path/to/samples.csv`` is replaced with your copy of ``samples.csv``. 
    - The default number of cores available to Snakemake is 1 which is enough for test data, but should probably be adjusted to 10+ for a real dataset.
    - Relative or absolute paths to the Snakefile and/or the working directory (if you're running elsewhere) are accepted!
```
python /path/to/camp_short-read-assembly/workflow/short-read-quality-control.py -d /path/to/work/dir -s /path/to/samples.csv
```

* Note: This setup allows the main Snakefile to live outside of the work directory.

Running on a slurm cluster
--------------------------
To run CAMP on a job submission cluster (for now, only Slurm is supported), use the following.
    - ``--slurm`` is an optional flag that submits all rules in the Snakemake pipeline as ``sbatch`` jobs. 
    - In Slurm mode, the ``-c`` flag refers to the maximum number of ``sbatch`` jobs submitted in parallel, **not** the pool of cores available to run the jobs. Each job will request the number of cores specified by threads in ``configs/resources/slurm.yaml``.
```
sbatch -J jobname -o jobname.log << "EOF"
#!/bin/bash
python /path/to/camp_short-read-quality-control/workflow/short-read-assembly.py --slurm \
   (-c max_number_of_parallel_jobs_submitted) \
    -d /path/to/work/dir \
    -s /path/to/samples.csv
EOF
```
Dependencies
------------
<LIST ALL DEPENDENCIES>

Credits
-------

* This package was created with `Cookiecutter <https://github.com/cookiecutter/cookiecutter>`_ as a simplified version of the `project template <https://github.com/audreyr/cookiecutter-pypackage>`_.
* Free software: MIT
* Documentation: https://short-read-quality-control.readthedocs.io. 


