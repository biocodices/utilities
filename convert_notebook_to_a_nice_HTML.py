#!/usr/bin/env python
"""This script will create a nice HTML version of your Jupyter notebook.
It needs Python grip installed (pip install grip).

Usage:
    convert_notebook_to_nice_HTML.py NOTEBOOK_PATH

"""
from os.path import join, dirname
from subprocess import run
from docopt import docopt


def main(arguments):
    # Create the markdown version of the notebook
    notebook = arguments['NOTEBOOK_PATH']
    command = 'jupyter nbconvert --to markdown %s' % notebook
    print(command, '\n')
    run(command.split(), check=True)

    # Export the markdown version to HTML
    markdown = notebook.replace('.ipynb', '.md')
    command = 'grip --export %s' % markdown
    print(command, '\n')
    run(command.split(), check=True)

    html = markdown.replace('.md', '.html')
    stylesheet_path = join(dirname(__file__), 'exported_notebooks.css')
    replace_pattern = "s#<link rel=\"stylesheet\" href=\"//octicons.github.com/components/octicons/octicons/octicons.css\" />#<link rel=\"stylesheet\" href=\"%s\" />#" % stylesheet_path
    command_args = ['sed', '-i', replace_pattern, html]
    print(' '.join(command_args), '\n')
    run(command_args, check=True)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
