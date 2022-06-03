import time
from unittest import TestCase

from mockito import mock, when, unstub, verify

from domain.containers import StoreImageScreenRegionUseCaseContainer
from domain.entities import Image
from domain.exceptions import ImageNotInScreenException
from domain.ports import ScreenReaderPort, PrinterServicePort
from domain.use_cases import LocateImageInScreenUseCase
from domain.value_objects import ImagePath, ScreenRegion


class TestLocateImageInScreenUseCase(TestCase):
    def setUp(self) -> None:
        self.printer_mock = mock(PrinterServicePort)
        when(self.printer_mock).print_line(...)
        when(self.printer_mock).print_open_line(...)
        when(self.printer_mock).close_line()

        self.screen_reader_mock = mock(ScreenReaderPort)

        self.container = StoreImageScreenRegionUseCaseContainer(
            screen_reader=self.screen_reader_mock,
            printer=self.printer_mock
        )

        self.image_path_mock = mock(ImagePath)
        self.image_path_mock.file_name = 'fake_file_name.py'

        self.image_mock = mock(Image)
        self.image_mock.name = 'image_name'
        self.image_mock.path = self.image_path_mock

        self.screen_region_mock = mock(ScreenRegion)
        when(self.screen_region_mock).to_string().thenReturn('')

        when(time).sleep(...)

    def tearDown(self) -> None:
        unstub()

    def store_region(self, screen_region: ScreenRegion) -> None:
        pass

    def test_execute_WHEN_image_found_THEN_sets_expected_screen_region_to_image_location(self) -> None:
        when(self.screen_reader_mock).get_image_location(self.image_mock).thenReturn(self.screen_region_mock)
        when(self).store_region(self.screen_region_mock)
        locate_image_in_screen_service = LocateImageInScreenUseCase(
            container=self.container,
            max_tries=1,
            seconds_between_tries=0
        )

        locate_image_in_screen_service.execute(
            image=self.image_mock
        )

        self.assertEqual(self.image_mock.location, self.screen_region_mock)

    def test_execute_WHEN_image_not_found_THEN_raises_image_not_in_screen_exception(self) -> None:
        when(self.screen_reader_mock).get_image_location(self.image_mock).thenRaise(ImageNotInScreenException)
        locate_image_in_screen_service = LocateImageInScreenUseCase(
            container=self.container,
            max_tries=1,
            seconds_between_tries=0
        )

        with self.assertRaises(ImageNotInScreenException):
            locate_image_in_screen_service.execute(self.image_mock)

    def test_execute_WHEN_image_not_found_THEN_try_again_as_many_times_as_defined(self) -> None:
        when(self.screen_reader_mock).get_image_location(self.image_mock).thenRaise(ImageNotInScreenException)
        locate_image_in_screen_service = LocateImageInScreenUseCase(
            container=self.container,
            max_tries=2,
            seconds_between_tries=0
        )

        try:
            locate_image_in_screen_service.execute(self.image_mock)
        except ImageNotInScreenException:
            pass

        verify(self.screen_reader_mock, times=2).get_image_location(self.image_mock)
