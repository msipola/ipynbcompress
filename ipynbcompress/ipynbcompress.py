# coding: utf-8
from base64 import b64decode, b64encode
from PIL import Image
from io import BytesIO
from os import stat
from nbformat import read, write

from IPython.core.display import Javascript
from IPython.display import display


def get_notebook_name():
    """Returns the name of the current notebook as a string
    
    """
    display(Javascript('IPython.notebook.kernel.execute("notebook_name = " + \
    "\'"+IPython.notebook.notebook_name+"\'");'))
    return notebook_name


def compress(filename=None, output_filename=None, img_width=2048, img_format='png'):
    """Compress images in IPython notebooks.

    Parameters
    ----------
    filename : string
        Notebook to compress. Will take any notebook format. If not given, will use the current notebook.
    output_filename : string
        If you do not want to overwrite your existing notebook, supply an
        filename for the new compressed notebook.
    img_width : int
        Which width images should be resized to.
    img_format : string
        Which compression to use on the images, valid options are
        *png* and *jpeg* (**requires libjpeg**).

    Returns
    -------
    int
        Size of new notebook in bytes.
    """
    if filename == None:
        filename = get_notebook_name()
        filename = get_notebook_name() #first time doesn't somehow work in notebook, might be known bug
    orig_filesize = stat(filename).st_size

    # compress images
    nb = read(filename, as_version=4)
    outputs = [cell.get('outputs', []) for cell in nb['cells']]
    # omit empty outputs
    outputs = [o for o in outputs if len(o)]
    # flatten
    outputs = [o for lines in outputs for o in lines]
    for output in outputs:
        data = output.get('data', {})
        if not data:
            continue
        keys = data.copy().keys()
        for key in list(keys):
            if 'image' in key:
                string = ''.join(data[key])
                bytes_img = b64decode(string)
                io_img = BytesIO(bytes_img)
                img = Image.open(io_img)
                out = BytesIO()
                img.save(out, img_format)
                out.seek(0)
                mime = 'image/' + img_format
                del data[key]
                data[mime] = b64encode(out.read()).decode('ascii')

    # save notebook
    if not output_filename:
        output_filename = filename
    try:
        output_format = nb.metadata.orig_nbformat
    except AttributeError:
        output_format = 4
    write(nb, output_filename, version=output_format)

    # calculate bytes saved
    bytes_saved = orig_filesize - stat(output_filename).st_size
    if bytes_saved <= 0:
        return print('%s: warning: no compression - %s bytes gained' % (filename, -bytes_saved))
    else:
        return print('%s: %s bytes saved' %(filename,bytes_saved))
