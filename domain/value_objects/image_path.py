import os
import sys
from pathlib import Path

from domain.exceptions import ImagePathException


class ImagePath:
    __STATIC_DIR = ''
    __VALID_EXTENSIONS = ['jpg', 'png']
    __file_name: str
    value: str

    def __init__(self, file_name: str) -> None:
        self.__set_static_dir()
        self.__validate_extension(file_name)
        absolute_path = self.__get_absolute_path(file_name)
        self.__validate_path_exists(absolute_path)
        self.value = absolute_path
        self.__file_name = file_name

    @property
    def file_name(self) -> str:
        return self.__file_name

    @staticmethod
    def get_static_dir_path() -> str:
        if not ImagePath.__STATIC_DIR:
            ImagePath.__set_static_dir()
        return ImagePath.__STATIC_DIR

    @staticmethod
    def __set_static_dir() -> None:
        if not ImagePath.__STATIC_DIR:
            domain_dir_name = 'domain'
            this_dir = Path(__file__).parent
            while not this_dir.name == domain_dir_name:
                this_dir = this_dir.parent
            domain_dir = this_dir
            ImagePath.__STATIC_DIR = f'{domain_dir}\\static'

    @staticmethod
    def __get_absolute_path(relative_path: str) -> str:
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("".join(ImagePath.__STATIC_DIR)), relative_path)

    @staticmethod
    def __validate_path_exists(absolute_path: str) -> None:
        if not os.path.isfile(absolute_path):
            raise ImagePathException(
                f'Path is not a file: {absolute_path}'
            )

    @staticmethod
    def __validate_extension(file_name: str) -> None:
        extension = file_name.split('.')[-1]
        if extension not in ImagePath.__VALID_EXTENSIONS:
            raise ImagePathException(
                f'Invalid extension: {extension}. Valid extensions are: {ImagePath.__VALID_EXTENSIONS}'
            )