# ipynbcompress

![project unmaintained](https://img.shields.io/badge/project-unmaintained-red.svg)

_**Note**: this project is sparcely maintained._

## Overview

So you have included an image with `IPython.display.Image()` and the file size
of your IPython Notebook got huge? No problem! This package will resize images
in your notebook and compress them as PNG or JPEG. Images are only resized if
they are above the specified width. 2048px and PNG compression is the default,
which should give relative high quality images and normal sized notebooks. JPEG
compression is nice if you serve the notebooks over the web (eg nbviewer) and
prefer fast loading times.

## Installation

Install the latest version from Github:

```bash
pip install git+https://github.com/msipola/ipynbcompress.git
```

## Example
From command line:
```sh
$ ipynb-compress notebook4.ipynb
notebook4.ipynb: 10 megabytes decrease
$ find . -name "*ipynb" -size +2M -exec ipynb-compress {} \;
./lab 03.21/automated scan.ipynb: warning: no compression - 0 bytes gained
./lab 03.21/automated scan.ipynb: compression less than 100k bytes - keeping original
./lab 03.21/trouble.ipynb: 9 megabytes decrease
...
```

In python:
```python
>>> import os
>>> from ipynbcompress import compress
>>> filename = '/path/to/notebook.ipynb'
>>> out = '/path/to/compressed.ipynb'
>>> # original size
... os.stat(filename).st_size
11563736
>>> # return bytes saved
... compress(filename, output_filename=out, img_width=800, img_format='jpeg')
11451545
>>> compress(filename, output_filename=out, img_width=800, img_format='png')
11205762
>>> # defaults to img_width = 2048px and png compression
... compress(filename, output_filename=out)
11411377
>>> # overwrite existing notebook
... compress(filename)
11411377
```

## API reference

API reference is at http://ipynbcompress.rtfd.org.

## Development
Install dependencies and link development version of ipynbcompress to pip:
```bash
git clone https://github.com/arve0/ipynbcompress
cd ipynbcompress
pip install -r requirements.txt # install dependencies and ipynbcompress-package
```

### Testing
```bash
tox
```

### Build documentation locally
To build the documentation:
```bash
pip install -r docs/requirements.txt
make docs
```



[build-status-image]: https://secure.travis-ci.org/arve0/ipynbcompress.png?branch=master
[travis]: http://travis-ci.org/arve0/ipynbcompress?branch=master
[pypi-version]: https://img.shields.io/pypi/v/ipynbcompress.svg
[pypi]: https://pypi.python.org/pypi/ipynbcompress
[wheel]: https://img.shields.io/pypi/wheel/ipynbcompress.svg
