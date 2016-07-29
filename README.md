# Scripts
Add this repo to your `$PATH` to use the scripts in the command line.
You need python 3.5 for all scripts and `docopt`.

## Convert a Jupyter Notebook to a nice HTML version
You need python 3.5 and the lastest version of `grip` (`pip install git+https://github.com/joeyespo/grip`). I assume you already have `jupyter` installed if you're dealing with notebooks.

`convert_notebook_to_a_nice_HTML.py NOTEBOOK_PATH`

The script will create both a markdown (`.md`) version of the notebook using `jupyter nbconvert --to markdown`, and then a nicely formatted HTML version using `grip --export`. Files will be located in the same directory and with the same basename.

## VCF to CSV
You need to have `biocodices` python package installed. Follow instructions there:
https://github.com/biocodices/biocodices/

`vcf_to_csv.py -n 6 samples-1.vcf samples-2.vcf`

The script will create a CSV file for each of the VCFs. By default, it will run
in 4 parallel processes (one VCF conversion per process), but you can specify
the number of parallel processes to run with.

The resulting CSV will have a "tidy data" format, with one observation per row.
That is, if you have a VCF with 10 markers and 10 samples, the CSV will have 
100 rows corresponding to 100 genotypes with their depth and quality data.

I'm not putting the non-genotypic info of the VCF in the CSV.

## Unzip and rename fastq.gz files
This script will unzip every fastq.gz file in the directory where it's run.
Afterwards, it will try to rename the unzipped files leaving the DNA-tags
that it can extract from the original filename.
The script assumes INTA IDs like "SAR123-<dna-tag-here>_S1_L001_R1_001.fastq.gz"
where the dna-tag part and the R1 or R2 bits will be kept.

To use it, just `cd` into the directory with the `.fastq.gz` files and run it:

`./unzip_and_rename_fastqs.py`
