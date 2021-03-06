# Scripts
Add this repo to your `$PATH` to use the scripts in the command line.
You need python 3.5 for all scripts and `docopt`.

## Convert a Jupyter Notebook to a nice HTML version
You need python 3.5 and the lastest version of `grip` (`pip install git+https://github.com/joeyespo/grip`). I assume you already have `jupyter` installed if you're dealing with notebooks.

`convert_notebook_to_a_nice_HTML.py NOTEBOOK_PATH`

The script will create both a markdown (`.md`) version of the notebook using `jupyter nbconvert --to markdown`, and then a nicely formatted HTML version using `grip --export`. Files will be located in the same directory and with the same basename.

## Unzip and rename fastq.gz files
This script will unzip every fastq.gz file in the directory where it's run.
Afterwards, it will try to rename the unzipped files leaving the DNA-tags
that it can extract from the original filename.
The script assumes INTA IDs like "SAR123-<dna-tag-here>_S1_L001_R1_001.fastq.gz"
where the dna-tag part and the R1 or R2 bits will be kept.

To use it, just `cd` into the directory with the `.fastq.gz` files and run it:

`./unzip_and_rename_fastqs.py`

## PED to Haploview

PLINK's formating with the `--recode HV` option is not enough for Haploview to read the files. At least I get errors with those files. The fix consists of replacing tabs with spaces, except between alleles of the same genotypes.

This script deals with that:

`./ped_to_haploview.py <ped_file>`

Keep in mind that the ped_file has to be generated with PLINK's `--recode HV`.
