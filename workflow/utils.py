'''Utilities.'''


# --- Workflow setup --- #


import os
from os import makedirs, symlink
from os.path import exists, join
import pandas as pd


def ingest_samples(samples, tmp):
    df = pd.read_csv(samples, header = 0, index_col = 0) 
    s = list(df.index)
    lst = df.values.tolist()
    for f in os.listdir(tmp):
        os.system("rm -rf " + join(tmp, f))
    for i,l in enumerate(lst):
        symlink(l[0], join(tmp, s[i] + '_1.fastq.gz'))
        symlink(l[1], join(tmp, s[i] + '_2.fastq.gz'))
    return s

class Workflow_Dirs:
    '''Management of the working directory tree.'''
    OUT = ''
    TMP = ''
    LOG = ''

    def __init__(self, work_dir, module):
        self.OUT = join(work_dir, "short-read-assembly")
        self.TMP = join(work_dir, 'tmp') 
        self.LOG = join(work_dir, 'logs') 
        if not exists(self.OUT):
            makedirs(self.OUT)
        if not exists(self.TMP):
            makedirs(self.TMP)
        if not exists(self.LOG):
            # Add custom subdirectories to organize rule logs
            makedirs(self.LOG)


# --- Workflow functions --- #


