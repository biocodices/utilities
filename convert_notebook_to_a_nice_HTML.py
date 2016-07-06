#!/usr/bin/env python
"""This script will create a nice HTML version of your Jupyter notebook.
It needs Python grip installed (pip install grip).

Usage:
    convert_notebook_to_nice_HTML.py NOTEBOOK_PATH [options]

Options:
    -h --help       Show this screen.
    --md-exists     Don't convert to markdown, assume the .md file is already
                    there.
    --html-exists   Don't use grip to convert to HTML, assume the HTML is
                    already there.
"""
from subprocess import run
from docopt import docopt


def main(arguments):
    notebook = arguments['NOTEBOOK_PATH']
    if not arguments['--md-exists']:
        # Create the markdown version of the notebook
        command = 'jupyter nbconvert --to markdown %s' % notebook
        print('\n*', command)
        run(command.split(), check=True)

    markdown = notebook.replace('.ipynb', '.md')
    if not arguments['--html-exists']:
        # Export the markdown version to HTML
        command = 'grip --export %s' % markdown
        print('\n*', command)
        run(command.split(), check=True)

    # Replace the stylesheet
    html = markdown.replace('.md', '.html')
    stylesheet_tag = """
<style>
    body .container {width: 97%;}
    body .markdown-body table { display: table; border: 2px solid silver; width: auto; font-size: 0.8em; line-height: 1; }
    body .markdown-body table th, .markdown-body table td { padding: 5px; }
    img { max-width: 1200px !important; }
</style>
""".replace('\n', ' ')
    replace_pattern = "s#<link rel=\"stylesheet\" href=\"//octicons.github.com/components/octicons/octicons/octicons.css\" />#%s#" % stylesheet_tag
    command_args = ['sed', '-i', replace_pattern, html]
    print('\n*', ' '.join(command_args))
    run(command_args, check=True)

    # Centered vertical alignment for combined cells in tables
    replace_pattern = 's/valign="top"/valign="center"/'
    command_args = ['sed', '-i', replace_pattern, html]
    print('\n*', ' '.join(command_args))
    run(command_args, check=True)

    print()
    print('Done!\n')


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
