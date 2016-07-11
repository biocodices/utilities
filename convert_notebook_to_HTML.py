#!/usr/bin/env python
"""This script will create a nice HTML version of your Jupyter notebook.
It needs Python grip installed (pip install grip).

Usage:
    convert_notebook_to_HTML.py NOTEBOOK_PATH [--zip]

Options:
    -h --help       Show this screen.
    -z --zip        Add the HTML and it's aux directory to a .zip file
                    so you can send it easily over the webz.
"""
from os import remove
from subprocess import run
from docopt import docopt


def main(arguments):
    notebook = arguments['NOTEBOOK_PATH']

    # Create the markdown version of the notebook
    command = 'jupyter nbconvert --to markdown %s' % notebook
    print('\n*', command)
    run(command.split(), check=True)

    # Export the markdown version to HTML
    markdown = notebook.replace('.ipynb', '.md')
    command = 'grip --export %s' % markdown
    print('\n*', command)
    run(command.split(), check=True)

    # Remove the markdown file when done
    remove(markdown)

    # Replace the stylesheet in the HTML
    # FIXME: improve this
    html = markdown.replace('.md', '.html')
    stylesheet_tag = """
<style>
    body .container {width: 97%;}
    body .markdown-body table { display: table; border: 2px solid silver; width: auto; font-size: 0.8em; line-height: 1; }
    body .markdown-body .highlight pre, .markdown-body pre { background-color: #d9d9d9; }
    body .markdown-body table th, .markdown-body table td { padding: 5px; }
    img { max-width: 1200px !important; }
</style>
""".replace('\n', ' ')
    replace_pattern = "s$<link rel=\"stylesheet\" href=\"//octicons.github.com/components/octicons/octicons/octicons.css\" />$%s$" % stylesheet_tag
    command_args = ['sed', '-i', replace_pattern, html]
    print('\n*', ' '.join(command_args))
    run(command_args, check=True)

    # Centered vertical alignment for combined cells in tables
    replace_pattern = 's/valign="top"/valign="center"/'
    command_args = ['sed', '-i', replace_pattern, html]
    print('\n*', ' '.join(command_args))
    run(command_args, check=True)

    if arguments['--zip']:
        # Zip both the HTML file and it's aux folder to send them easily
        # The aux folder is added by `grip --export` with a "_files" suffix.
        command = 'zip {zip_file} {html} {aux_dir}'.format(**{
            'html': html,
            'aux_dir': html.replace('.html', '') + '_files',
            'zip_file': html.replace('.html', '.zip')
        })
        print('\n*', command)
        run(command.split(), check=True)

    print()
    print('Done!\n')


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
