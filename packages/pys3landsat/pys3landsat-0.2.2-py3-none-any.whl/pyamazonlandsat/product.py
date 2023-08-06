import attr
import os
import tarfile

from pyamazonlandsat.utils import get_path_row_from_name
from pyamazonlandsat.downloader import Downloader


@attr.s
class Product:
    """Class that represent a Product
    :param name: name of the Product.
    type name: str.
    :param output_path: path where save the downloaded prodcuct.
    :type output_path: str.
    """
    name = attr.ib()
    output_path = attr.ib()
    _path_files = attr.ib(init=False)
    _link = attr.ib(init=False,
                     default='https://landsat-pds.s3.amazonaws.com/c1/L8/%s/%s/%s')

    def _generate_link(self):
        """Method to generate the link to download from S3
        Amazon Service
        """
        path, row = get_path_row_from_name(self.name)
        self._link = self._link % (path, row, self.name)

    def _compress_product(self):
        """Method to compress product into a tar file.
        """
        with tarfile.open('%s.tar.gz' %
                          os.path.join(self.output_path, self.name), 'w:gz') as tar:
            for ff in os.listdir(self._path_files):
                tar.add(
                    os.path.join(
                    self._path_files, ff),
                    ff)

    def get_image_product(self):
        """Method to download the product.

        This method create a `Downloader`_ object and download
        the images. Then compressed it and move to `output_path`

        The downloaded images are saved into a temporal folder,
        then is compresed into a tar file and then move to
        `output_path`.
        """
        self._generate_link()
        downloader = Downloader(self._link)
        self._path_files = downloader.download_images()
        self._compress_product()
