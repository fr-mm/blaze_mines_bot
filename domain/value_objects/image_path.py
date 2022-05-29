import os
import sys
from pathlib import Path

from domain.exceptions import ImagePathException
from domain import static


class ImagePath:
    __VALID_EXTENSIONS = ['jpg', 'png']
    __static_directory: str = None
    __file_name: str
    __value: str

    def __init__(self, file_name: str) -> None:
        self.__validate_extension(file_name)
        absolute_path = self.__get_absolute_path(file_name)
        self.__validate_path_exists(absolute_path)
        self.__value = absolute_path
        self.__file_name = file_name

    @property
    def value(self) -> str:
        return self.__value

    @property
    def file_name(self) -> str:
        return self.__file_name

    @staticmethod
    def get_static_directory_path() -> str:
        if not ImagePath.__static_directory:
            ImagePath.__set_static_directory_path()
        return ImagePath.__static_directory

    @staticmethod
    def __get_absolute_path(file_name: str) -> str:
        static_directory = ImagePath.get_static_directory_path()
        return os.path.join(static_directory, file_name)

    @staticmethod
    def __set_static_directory_path() -> None:
        if hasattr(sys, '_MEIPASS'):
            return os.path.abspath(sys._MEIPASS)
        static_dir = Path(static.__file__).parent
        ImagePath.__static_directory = os.path.abspath(static_dir)

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
