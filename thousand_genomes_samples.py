#!/usr/bin/env python

"""
Download the sample data (IDs, population, super population, gender) for the
2,504 samples of The 1000 Genomes Project.

If you run this as a script, it will print CSV lines to STDOUT.

If you use it as a Python module, just do:

    from thousand_genomes_samples import get_thousand_genomes_samples

Usage:
    thosand_genomes_samples.py [-h | --help]
"""

import sys
from os.path import expanduser, join, isfile

import requests
from docopt import docopt


BASE_URL = 'http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/'
LOCAL_FILE = expanduser('~/.thousand_genomes_samples.csv')


def get_thousand_genomes_samples():
    if not isfile(LOCAL_FILE):
        response = requests.get(join(BASE_URL,
            'integrated_call_samples_v3.20130502.ALL.panel'))

        with open(LOCAL_FILE, 'w') as f:
            for line in response.text.split('\n'):
                fields = [field for field in line.split('\t') if field]
                f.write(','.join(fields) + '\n')

    with open(LOCAL_FILE) as f:
        for line in f.read().split('\n'):
            print(line)

def main():
    docopt(__doc__)
    get_thousand_genomes_samples()

if __name__ == '__main__':
    main()
