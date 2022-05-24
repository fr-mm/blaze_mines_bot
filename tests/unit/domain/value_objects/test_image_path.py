from unittest import TestCase

from domain.exceptions import InvalidImagePathException
from domain.value_objects import ImagePath


class TestImagePath(TestCase):
    def test_init_WHEN_valid_file_name_THEN_creates_instance(self) -> None:
        file_name = 'example_target.jpg'

        ImagePath(file_name)

    def test_init_WHEN_file_does_not_exists_THEN_raises_invalid_image_path_exception(self) -> None:
        file_name = 'fake_file_name.jpg'

        with self.assertRaises(InvalidImagePathException):
            ImagePath(file_name)

    def test_init_WHEN_invalid_extension_THEN_raises_invalid_image_path_exception(self) -> None:
        file_name = '__init__.py'

        with self.assertRaises(InvalidImagePathException):
            ImagePath(file_name)
