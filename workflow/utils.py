'''Utilities.'''


# --- Workflow setup --- #


import gzip
import os
from os import makedirs, symlink, system
from os.path import abspath, basename, exists, join
import pandas as pd
import shutil


def ingest_samples(samples, tmp):
    df = pd.read_csv(samples, header = 0, index_col = 0) 
    s = list(df.index)
    lst = df.values.tolist()
    for i,l in enumerate(lst):
        print(l[0])
        if not exists(join(tmp, s[i] + '_1.fastq.gz')):
            symlink(l[0], join(tmp, s[i] + '_1.fastq.gz'))
            symlink(l[1], join(tmp, s[i] + '_2.fastq.gz'))
    return s


class Workflow_Dirs:
    '''Management of the working directory tree.'''
    OUT = ''
    TMP = ''
    LOG = ''

    def __init__(self, work_dir, module):
        self.OUT = join(work_dir, module)
        self.TMP = join(work_dir, 'tmp') 
        self.LOG = join(work_dir, 'logs') 
        if not exists(self.OUT):
            makedirs(self.OUT)
            makedirs(join(self.OUT, '0_metaspades'))
            makedirs(join(self.OUT, '1_megahit'))
            makedirs(join(self.OUT, 'final_reports'))
        if not exists(self.TMP):
            makedirs(self.TMP)
        if not exists(self.LOG):
            # Add custom subdirectories to organize rule logs
            makedirs(self.LOG)
            makedirs(join(self.LOG, 'metaspades'))
            makedirs(join(self.LOG, 'megahit'))


def cleanup_files(work_dir, df):
    smps = list(df.index)
    for s in smps:
        ms_dir = join(work_dir, 'short-read-assembly', '0_metaspades', s)
        if exists(ms_dir):
            system('rm -rf ' + join(ms_dir, 'K21'))
            system('rm -rf ' + join(ms_dir, 'K33'))
            system('rm -rf ' + join(ms_dir, 'K55'))


def print_cmds(log):
    fo = basename(log).split('.')[0] + '.cmds'
    lines = open(log, 'r').read().split('\n')
    fi = [l for l in lines if l != '']
    write = False
    with open(fo, 'w') as f_out:
        for l in fi:
            if 'rule' in l:
                f_out.write('# ' + l.strip().replace('rule ', '').replace(':', '') + '\n')
            if 'wildcards' in l: 
                f_out.write('# ' + l.strip().replace('wildcards: ', '') + '\n')
            if 'resources' in l:
                write = True 
                l = ''
            if '[' in l: 
                write = False 
            if write:
                f_out.write(l.strip() + '\n')
            if 'rule make_config' in l:
                break


# --- Workflow functions --- #


