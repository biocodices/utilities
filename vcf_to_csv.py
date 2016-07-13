#!/usr/bin/env python
"""This script will create a CSV version of one or more VCF files. In the CSV,
the genotype fields (usually DP, AD, GQ) will be treated as separate columns
and there will be one row per "observation" --i.e. per genotype--, following
the idea of "tidy data". So if you have 10 markers and 10 samples, the CSV
will have 100 rows. Have in mind that the structure of the CSV table does not
mirror the strcture of the VCF.

Usage:
    vcf_to_csv.py [-n PROCESSES] VCF_FILE...

Example:
    vcf_to_csv.py -n 8 *.vcf

Options:
    -n PROCESSES      Number of parallel processes to spawn. Default: 4.
"""

from os.path import isfile
from docopt import docopt
from multiprocessing import Pool
from biocodices.variant_calling import VcfMunger


def main(arguments):
    print('Starting process on %s VCFs.' % len(arguments['VCF_FILE']))
    print('Running in parallel x%s.' % arguments['-n'])
    print()

    with Pool(int(arguments['-n'])) as pool:
        results = []
        for vcf_filepath in arguments['VCF_FILE']:
            result = pool.apply_async(vcf_to_frame, (vcf_filepath,))
            results.append(result)

        for result in results: result.get()

    print()
    print('Done!')


def vcf_to_frame(vcf_filepath):
    print(' * Reading %s (might take a while for large files)' % vcf_filepath)
    _, tidy_df = VcfMunger.vcf_to_tidy_dataframe(vcf_filepath)

    csv_filepath = output_filename(vcf_filepath)
    print(' * Saving %s' % csv_filepath)
    tidy_df.to_csv(csv_filepath)


def output_filename(input_filename):
    if input_filename.endswith('.vcf'):
        output = input_filename.replace('.vcf', '.csv')
    else:
        output = input_filename + '.csv'

    if isfile(output):
        return output + '~'

    return output


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if not arguments['-n']:
        arguments['-n'] = 4

    main(arguments)
