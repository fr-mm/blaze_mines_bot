from unittest import TestCase

from domain.exceptions import ImageNameException
from domain.value_objects import ImageName


class TestImageName(TestCase):
    def test_init_WHEN_valid_value_given_THEN_creates_instance_with_given_value(self) -> None:
        valid_value = 'name'

        image_name = ImageName(value=valid_value)

        self.assertEqual(image_name.value, valid_value)

    def test_init_WHEN_value_is_empty_string_THEN_raises_image_name_exception(self) -> None:
        invalid_value = ''

        with self.assertRaises(ImageNameException):
            ImageName(value=invalid_value)
