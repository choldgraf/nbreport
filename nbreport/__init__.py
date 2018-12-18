import argparse
from nbclean import NotebookCleaner
import nbformat as nbf
import os.path as op
import subprocess
import os

__version__ = 'v0.1'
path_template = op.join(op.dirname(__file__), 'static', 'report.tpl')


def _jupyter_bundlerextension_paths():
    """The nbreport extension!"""
    return [{
        'name': 'nbreport',                         # unique bundler name
        'label': 'NBReport',                        # human-redable menu item label
        'module_name': 'nbreport',                  # module containing bundle()
        'group': 'download'                         # group under 'deploy' or 'download' menu
    }]

def bundle(handler, model):
    """Transform, convert, bundle, etc. the notebook referenced by the given
    model.

    Then issue a Tornado web response using the `handler` to redirect
    the user's browser, download a file, show a HTML page, etc. This function
    must finish the handler response before returning either explicitly or by
    raising an exception.

    Parameters
    ----------
    handler : tornado.web.RequestHandler
        Handler that serviced the bundle request
    model : dict
        Notebook model from the configured ContentManager
    """
    # Return the buffer value as the response
    abs_nb_path = op.join(handler.settings['contents_manager'].root_dir, model['path'])
    notebook_filename = model['name']
    path_out = op.join(op.dirname(abs_nb_path), notebook_filename)
    generate_report(model['content'], path_out)

    css = model['content']['metadata'].get('css_extra')
    if css:
        path_to_nb_dir = op.relpath(op.dirname(model['path']), op.curdir)
        path_css = op.join(path_to_nb_dir, css)

        if not op.exists(path_css):
            raise ValueError("Could not find CSS file: {}".format(path_css))
        _extra_css(path_out.replace('.ipynb', '.html'), path_css)

    output_temp = "<h1 style='padding-top: 300px; text-align: center;'>{}<br />" + "{}</h1>".format(path_out.replace('.ipynb', '.html'))
    if op.exists(path_out.replace('.ipynb', '.html')):
        output = output_temp.format("Report generated at the file below")
    else:
        output = output_temp.format("<strong>Report failed</strong> to generated the file below")
    handler.finish(output)


def generate_report(ntbk, path_out):

    # Clean up the notebook
    cleaner = NotebookCleaner(ntbk)
    cleaner.remove_cells(empty=True)
    cleaner.remove_cells(search_text='hide_cell')
    cleaner.clear(kind="content", search_text='hide_code')
    cleaner.clear('stderr')

    path_out_tmp = path_out + '_TMP'
    cleaner.save(path_out_tmp)

    # Build the HTML
    call = ['jupyter', 'nbconvert',
            '--log-level="CRITICAL"',
            '--to', 'html',
            '--template', path_template,
            "--EmbedImagesPreprocessor.embed_images=True",
            "--TemplateExporter.exclude_input_prompt=True",
            "--TemplateExporter.exclude_output_prompt=True",
            '--FilesWriter.build_directory={}'.format(op.dirname(path_out)),
            path_out_tmp]
    subprocess.run(call)
    os.remove(path_out_tmp)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Path to the notebook for which you want to create a report.")
    parser.add_argument("--output_folder", default=None, help="The output folder for the HTML file.")
    parser.add_argument("--css", default=None, help="The path to a CSS file to include in the HTML.")

    args = parser.parse_args()
    path_in = args.input_path
    css = args.css
    ntbk = nbf.read(path_in, nbf.NO_CONVERT)
    output_folder = args.output_folder
    if args.output_folder is None:
        output_folder = op.dirname(path_in)
    output_path = op.join(output_folder, op.basename(path_in))
    generate_report(ntbk, output_path)
    _extra_css(output_path.replace('.ipynb', '.html'), css)

    print('Finished generating report for file: \n{}'.format(output_path))

def _extra_css(path_html, css):
    # Add extra CSS if possible
    if css:
        if not op.exists(css):
            raise ValueError("Could not find CSS file: {}".format(css))
        with open(path_html, 'r') as ff:
            lines = ff.readlines()

        # Read and add the new CSS lines
        with open(css, 'r') as ff:
            css_lines = ff.readlines()

        # Indent the added CSS
        css_lines = ['    ' + iline for iline in css_lines]
        css_lines = ['<style type="text/css">\n'] + css_lines
        css_lines += ['\n</style>']

        # Add in the CSS at the end of the file (but not the last line since it's </html>)
        lines = lines[:-2] + css_lines + lines[-2:]
        with open(path_html, 'w') as ff:
            ff.writelines(lines)

if __name__ == '__main__':
    main()
