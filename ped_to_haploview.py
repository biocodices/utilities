#!/usr/bin/env python
"""PED to Haploview format converter. This script converts a PED file generated with plink --recode HV to a format that Haploview can actually open. The fix consists of replacing spaces with tabs to separate fields, but separating alleles from the same genotype with a single space.

Usage:
    ped_to_haploview.py <pedfile>

"""

from docopt import docopt


def grouped(l, n):
    """Yield successive n-sized groups from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def ped_line_to_haploview_line(line):
    fields = line.split()
    sample_data = fields[:6]
    genotypes = fields[6:]

    # Join each genotype's alleles by a space
    genotypes = [' '.join(genotype) for genotype in grouped(genotypes, 2)]

    # Join different fields by tabs
    return '\t'.join(sample_data + genotypes)


def convert(pedfile, haploview_pedfile):
    print()

    print('* Reading %s' % pedfile)
    with open(pedfile) as ped:
        new_lines = [ped_line_to_haploview_line(line)
                     for line in ped.readlines()]

    print('* Writing %s' % haploview_pedfile)
    with open(haploview_pedfile, 'w') as hv_ped:
        for new_line in new_lines:
            hv_ped.write(new_line + '\n')

    print('\nDone!')


if __name__ == '__main__':
    pedfile = docopt(__doc__)['<pedfile>']

    if pedfile.endswith('.ped'):
        haploview_pedfile = pedfile.replace('.ped', '.haploview.ped')
    else:
        haploview_pedfile = pedfile + '.haploview.ped'

    convert(pedfile, haploview_pedfile)
