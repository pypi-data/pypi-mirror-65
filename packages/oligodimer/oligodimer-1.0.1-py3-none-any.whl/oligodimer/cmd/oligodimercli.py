#!/usr/bin/env python3

'''OligoDimer: Detecting dimers among multiple oligo sequences
Github: https://github.com/billzt/OligoDimer
This is a CLI script for OligoDimer
'''

import argparse
import re
import os
import sys
import json
import shutil

from distutils.version import LooseVersion

from oligodimer.core.multiplex import get_dimers
from oligodimer.core import version

def main():
    parser = argparse.ArgumentParser(description='primertool-junctions: preparing the exon-exon junction database for PrimerServer2', \
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version.get())
    parser.add_argument('oligos', help='oligo sequences file in TSV format', type=argparse.FileType('r'))
    parser.add_argument('-m', '--min-Tm', help='Report dimers formed above this Tm temperature.', default=35, type=int)
    parser.add_argument('-p', '--cpu-num', help='CPU num.', default=2)
    args = parser.parse_args()

    oligo_seqs = args.oligos.read()
    dimers = get_dimers(oligo_seqs, min_Tm=args.min_Tm, cpu=args.cpu_num)
    if 'error' in dimers:
        print(dimers)
        exit(0)
    print('#ID1', 'seq1', 'ID2', 'seq2', 'Tm', sep='\t')
    for dimer in dimers['dimers']:
        print(dimer[0]['id'], dimer[0]['seq'], dimer[1]['id'], dimer[1]['seq'], dimer[2], sep='\t')

if __name__ == "__main__":
    main()

