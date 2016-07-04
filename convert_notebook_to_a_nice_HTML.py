#!/usr/bin/env python
"""This script will create a nice HTML version of your Jupyter notebook.
It needs Python grip installed (pip install grip).

Usage:
    convert_notebook_to_nice_HTML.py NOTEBOOK_PATH

"""
from subprocess import run
from docopt import docopt


def main(arguments):
    # Create the markdown version of the notebook
    notebook = arguments['NOTEBOOK_PATH']
    command = 'jupyter nbconvert --to markdown %s' % notebook
    print('\n*', command)
    run(command.split(), check=True)

    # Export the markdown version to HTML
    markdown = notebook.replace('.ipynb', '.md')
    command = 'grip --export %s' % markdown
    print('\n*', command)
    run(command.split(), check=True)

    # Replace the stylesheet
    html = markdown.replace('.md', '.html')
    stylesheet_tag = '<style>body .container {width: 97%;}</style>'
    replace_pattern = "s#<link rel=\"stylesheet\" href=\"//octicons.github.com/components/octicons/octicons/octicons.css\" />#%s#" % stylesheet_tag
    command_args = ['sed', '-i', replace_pattern, html]
    print('\n*', ' '.join(command_args))
    run(command_args, check=True)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
