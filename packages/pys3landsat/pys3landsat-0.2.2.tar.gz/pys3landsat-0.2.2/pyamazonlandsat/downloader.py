import attr
import re
import os
import requests

from bs4 import BeautifulSoup
from urllib import request
from tempfile import mkdtemp


@attr.s
class Downloader:
    """Class that download the data from Amazon S3 Service.

    :param link: link to download the datas.
    :type link: str.
    """
    link = attr.ib()
    _html = attr.ib(init=False, default='')
    _soup = attr.ib(init=False, default=None)
    _links_tiff = attr.ib(init=False, default=list())
    _links_mtl_ang_files = attr.ib(init=False, default=list())
    _tmp_folder = attr.ib(init=False, default=mkdtemp())

    def __read_key_value(self, pattern):
        """Read the href links according to a `pattern`.

        :param pattern: patter to filter which data will be download.
        :type patter: str.
        :return: generator with the filtered link.
        :rtype: generator.
        """
        for link in self._soup.find_all('a'):
            value = link.get('href')
            if re.match(pattern, value):
                yield value

    def read_link(self):
        """Read  the page passed on `link` parameter.
        """
        self._html = request.urlopen('%s/index.html' % self.link).read()
        self._soup = BeautifulSoup(self._html, 'html.parser')

    def get_download_links_tiff(self):
        """get the links of tiff image to download.

        this use `__read_key_value`_ to filter just .tif files.
        """
        self._links_tiff = list(self.__read_key_value('.*.TIF$'))

    def get_mtl_ang_files(self):
        """get the links of mtl and ang files.

        this use `__read_key_value`_ to filter just .txt files.
        """
        self._links_mtl_ang_files = list(self.__read_key_value('.*.txt$'))

    def _prepare_for_download(self):
        """This method prepare the datas to download the product.self

        This run `read_link`_ method then `get_download_links_tiff`_ and
        then `get_mtl_ang_files`_ method.
        """
        self.read_link()
        self.get_download_links_tiff()
        self.get_mtl_ang_files()
        return True

    def _save_file_on_tmp_folder(self, name, content):
        """Save the binary `content` into a `name` file.

        The content is the requests content after read the download file.

        :param content:  binary stream with the content of the image or file.
        :type content: binary stream.
        :param name: name of the file where save the content.
        :type name: str.
        """
        with open(os.path.join(self._tmp_folder, name), 'wb') as f:
            f.write(content)

    def _download_file(self, name):
        """Download the image or file.

        This method make a get requests to download the image or file from
        S3 Amazon service.

        :param name: link to download.
        :type name: str.
        """
        file_content = requests.get('%s/%s' % (self.link, name))
        self._save_file_on_tmp_folder(name, file_content.content)

    def download_images(self):
        """Download the images or file.

        This method prepared the information to download the images or
        files. The download each images or files into a temp folder.

        Return the temp folder where the files are saved.

        :return: path to temporal folder wehre the failes are saved.
        :rtype: str.
        """
        self._prepare_for_download()
        for tiff in self._links_tiff:
            self._download_file(tiff)
        for txt in self._links_mtl_ang_files:
            self._download_file(txt)

        return self._tmp_folder
