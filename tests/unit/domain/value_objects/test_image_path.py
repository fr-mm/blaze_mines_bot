import os
from unittest import TestCase

from domain.exceptions import ImagePathException
from domain.value_objects import ImagePath


class TestImagePath(TestCase):
    def setUp(self) -> None:
        self.bomb_file_name = 'bomb.jpg'

    def test_init_WHEN_valid_file_name_THEN_creates_instance(self) -> None:
        file_name = self.bomb_file_name

        ImagePath(file_name)

    def test_value_WHEN_called_THEN_returns_valid_path(self) -> None:
        file_name = self.bomb_file_name
        image_path = ImagePath(file_name)

        result_value = image_path.value

        self.assertTrue(os.path.isfile(result_value))

    def test_value_WHEN_called_THEN_returns_valid_path_ending_with_file_name(self) -> None:
        file_name = self.bomb_file_name
        image_path = ImagePath(file_name)

        result_value = image_path.value

        result_file_name = os.path.split(result_value)[-1]
        self.assertEqual(result_file_name, file_name)

    def test_init_WHEN_file_does_not_exists_THEN_raises_invalid_image_path_exception(self) -> None:
        file_name = 'fake_file_name.jpg'

        with self.assertRaises(ImagePathException):
            ImagePath(file_name)

    def test_init_WHEN_invalid_extension_THEN_raises_invalid_image_path_exception(self) -> None:
        file_name = '__init__.py'

        with self.assertRaises(ImagePathException):
            ImagePath(file_name)

    def test_file_name_WHEN_called_THEN_returns_given_file_name(self) -> None:
        file_name = self.bomb_file_name
        image_path = ImagePath(file_name)

        result_file_name = image_path.file_name

        self.assertEqual(result_file_name, file_name)
