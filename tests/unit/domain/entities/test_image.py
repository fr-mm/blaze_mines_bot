from unittest import TestCase

from mockito import mock

from domain.entities import Image
from domain.exceptions import ImageLocationNotSetException
from domain.value_objects import ImageName, ImagePath, ScreenRegion


class TestImage(TestCase):
    def setUp(self) -> None:
        self.image_name = mock(ImageName)
        self.image_path = mock(ImagePath)
        self.screen_region = mock(ScreenRegion)

    def test_name_WHEN_valid_name_THEN_returns_given_name(self) -> None:
        image = Image(
            name=self.image_name,
            path=self.image_path,
            location=self.screen_region
        )

        self.assertEqual(image.name, self.image_name)

    def test_path_WHEN_valid_path_THEN_returns_given_name(self) -> None:
        image = Image(
            name=self.image_name,
            path=self.image_path,
            location=self.screen_region
        )

        self.assertEqual(image.path, self.image_path)

    def test_location_WHEN_valid_location_THEN_returns_given_name(self) -> None:
        image = Image(
            name=self.image_name,
            path=self.image_path,
            location=self.screen_region
        )

        self.assertEqual(image.location, self.screen_region)

    def test_location_location_WHEN_no_location_given_THEN_raises_image_location_not_set_exception(self) -> None:
        image = Image(
            name=self.image_name,
            path=self.image_path
        )

        with self.assertRaises(ImageLocationNotSetException):
            location = image.location

    def test_location_setter_WHEN_screen_region_given_THEN_sets_given_screen_region(self) -> None:
        image = Image(
            name=self.image_name,
            path=self.image_path
        )

        image.location = self.screen_region

        self.assertEqual(image.location, self.screen_region)
