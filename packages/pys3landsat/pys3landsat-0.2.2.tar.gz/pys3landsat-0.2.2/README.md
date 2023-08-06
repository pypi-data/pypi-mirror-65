# pyamazonlandsat


## Installation

To install you can use pypi:

```
$ pip install pys3landsat
````

or if you want to build and install from source:

```
$ git clone https://github.com/eamanu/pyamazonlandsat.git
$ python setup.py build
$ python setup.py install
```

## Usage

To use you must be know the name of the product to download

And just run the command:

```
$ pys3landsat -n LC08_L1TP_231080_20200128_20200210_01_T1 -o ~/download_products

```

For information of the parameters you could run –help

```
$ pys3landsat --help
usage: pys3landsat [-h] [-n NAME] [-o OUTPUT]

Download Landsat 8 images from Amazon S3

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of the product to download.
  -o OUTPUT, --output OUTPUT
                        Output path to the product.

````

# Contribution

Whole contributions are welcome, please feel free to send a PR or issue.


