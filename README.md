pyImageTools
====
[![Python3](https://img.shields.io/badge/python-3.7-blue.svg)](https://github.com/Der-Eddy/pyImageTools)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/Der-Eddy/pyImageTools/master/LICENSE)

A small script library to work with image folders.

    usage: imageTools.py [-h] program path

    Provides several tools to manage folders of images

    positional arguments:
    program     Specific tool you want to run (Default: dupe) Available
                programs: dupe, exactdupe
    path        Path of an image folder to test (Default: . / the path you are
                currently in)

    optional arguments:
    -h, --help  show this help message and exit

Programs
---

### dupe

`dupe` (`duplicates.py`) deletes duplicate images based on a similar hash and keeps the image with highest file size.

### cropBorder

`cropBorder` (`cropBorder.py`) removes any border (i.e. black border above and below) from an image.

### exactdupe

`exactdupe` deletes exact duplicates with the same MD5 hash.


Requirements
---

    Pillow
    imagehash
    progressbar2

LICENSE
---

    The MIT License (MIT)

    Copyright (c) 2018 Eduard Nikoleisen (Der-Eddy)

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
