'''Utilities.'''


# --- Workflow setup --- #


import gzip
import os
from os import makedirs, symlink, system, stat
from os.path import abspath, basename, exists, getsize, join
import pandas as pd
import shutil


def ingest_samples(samples, tmp):
    df = pd.read_csv(samples, header = 0, index_col = 0) # name, fwd, rev
    s = list(df.index)
    lst = df.values.tolist()
    for i,l in enumerate(lst):
        if not exists(join(tmp, s[i] + '_1.fastq.gz')):
            symlink(abspath(l[0]), join(tmp, s[i] + '_1.fastq.gz'))
            symlink(abspath(l[1]), join(tmp, s[i] + '_2.fastq.gz'))
    return s


def check_make(d):
    if not exists(d):
        makedirs(d)


class Workflow_Dirs:
    '''Management of the working directory tree.'''
    OUT = ''
    TMP = ''
    LOG = ''

    def __init__(self, work_dir, module):
        self.OUT = join(work_dir, module)
        self.TMP = join(work_dir, 'tmp') 
        self.LOG = join(work_dir, 'logs') 
        check_make(self.OUT)
        out_dirs = ['0_metaspades', '1_megahit', 'final_reports']
        for d in out_dirs: 
            check_make(join(self.OUT, d))
        check_make(self.TMP)
        check_make(self.LOG)
        log_dirs = ['metaspades', 'megahit']
        for d in log_dirs: 
            check_make(join(self.LOG, d))


def cleanup_files(work_dir, df):
    smps = list(df.index)
    for s in smps:
        ms_dir = join(work_dir, 'short-read-assembly', '0_metaspades', s)
        if exists(ms_dir):
            system('rm -rf ' + join(ms_dir, 'K21'))
            system('rm -rf ' + join(ms_dir, 'K33'))
            system('rm -rf ' + join(ms_dir, 'K55'))


def print_cmds(f):
    # fo = basename(log).split('.')[0] + '.cmds'
    # lines = open(log, 'r').read().split('\n')
    fi = [l for l in f.split('\n') if l != '']
    write = False
    with open('commands.sh', 'w') as f_out:
        for l in fi:
            if 'rule' in l:
                f_out.write('# ' + l.strip().replace('rule ', '').replace(':', '') + '\n')
                write = False
            if 'wildcards' in l:
                f_out.write('# ' + l.strip().replace('wildcards: ', '') + '\n')
            if 'resources' in l:
                write = True
                l = ''
            if write:
                f_out.write(l.strip() + '\n')
            if 'rule make_config' in l:
                break


# --- Workflow functions --- #

