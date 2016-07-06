# Scripts
Add this repo to your `$PATH` to use the scripts in the command line.

## Convert a Jupyter Notebook to a nice HTML version
You need python 3.5 and the lastest version of `grip` (`pip install git+https://github.com/joeyespo/grip`). I assume you already have `jupyter` installed if you're dealing with notebooks.

`convert_notebook_to_a_nice_HTML.py NOTEBOOK_PATH`

The script will create both a markdown (`.md`) version of the notebook using `jupyter nbconvert --to markdown`, and then a nicely formatted HTML version using `grip --export`. Files will be located in the same directory and with the same basename.
