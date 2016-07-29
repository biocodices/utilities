#!/usr/bin/env python

import re
import subprocess
import sys
from os import rename
from os.path import isfile
from glob import glob


# Pattern to extract the INTA ID and DNA-tag from the fastq filenames
PATTERNS = [
    r'(SAR\d+).*-(\d+-\d+).*_(R\d)',
    #  r'(sar\d+).*01(\d{5}).*_(R\d)',
    #  r'(sar\d+).*ENPv1[-_](\d{5}).*_(R\d)',
]


# This script unzips the fastq.gz files in the directory where it's run
# and the renames the unzipped files keeping just the DNA-tag.
# The original fastq.gz files are left untouched and the unzip versions
# will sit in the same directory afterwards.
def main():
    print('\nUnzipping the fastq.gz files\n')
    for zipped_filename in glob('*.fastq.gz'):
        if any(substr in zipped_filename for substr in ['cont', 'Cont']):
            continue  # Skip controls

        unzipped_filename = zipped_filename.replace('.fastq.gz', '.fastq')
        if isfile(unzipped_filename):
            print('Exists: %s' % unzipped_filename)
            continue
        command = 'gzip -dc %s' % zipped_filename

        with open(unzipped_filename, 'w') as new_file:
            print(command + ' > ' + unzipped_filename)
            subprocess.run(command.split(' '), stdout=new_file, check=True)

    print('\nRenaming the unzipped fastqs with sample IDs\n')
    for fn in glob('*.fastq'):
        for pattern in PATTERNS:
            match = re.search(pattern, fn)
            if match: break  # Keep the first successful match

        if not match:
            print("(!) Please add a PATTERN to match this {}\n".format(fn))
            sys.exit()

        inta_sample_id, sample_id, read_number = match.groups(1)
        print('%s -> %s' % (inta_sample_id, sample_id))
        new_fn = 'dna_{}.{}.fastq'.format(sample_id, read_number)

        if isfile(new_fn):
            msg = ('(!) File {} already exists.\n\n'
                   'Repeated sample ID? Check '
                   'the input fastq files for sample {}/{}.')
            print(msg.format(new_fn, inta_sample_id, sample_id))
            sys.exit()

        print(fn + ' -> ' + new_fn)
        rename(fn, new_fn)


if __name__ == '__main__':
    main()
