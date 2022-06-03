import time
from unittest import TestCase

from mockito import mock, when, unstub, verify

from domain.containers import StoreImageScreenRegionUseCaseContainer
from domain.exceptions import ImageNotInScreenException
from domain.ports import ScreenReaderPort, PrinterServicePort
from domain.use_cases import StoreImageScreenRegionUseCase
from domain.value_objects import ImagePath, ScreenRegion


class TestStoreImageScreenRegionUseCase(TestCase):
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

        self.screen_region_mock = mock(ScreenRegion)
        when(self.screen_region_mock).to_string().thenReturn('')

        when(time).sleep(...)

    def tearDown(self) -> None:
        unstub()

    def store_region(self, screen_region: ScreenRegion) -> None:
        pass

    def test_execute_WHEN_image_found_THEN_calls_store_region_with_expected_location(self) -> None:
        when(self.screen_reader_mock).get_image_location(self.image_path_mock).thenReturn(self.screen_region_mock)
        when(self).store_region(self.screen_region_mock)
        get_image_screen_region_use_case = StoreImageScreenRegionUseCase(
            container=self.container,
            max_tries=1,
            seconds_between_tries=0
        )

        get_image_screen_region_use_case.execute(
            image=self.image_path_mock,
            store_region=self.store_region
        )

        verify(self).store_region(self.screen_region_mock)

    def test_execute_WHEN_image_not_found_THEN_raises_image_not_in_screen_exception(self) -> None:
        when(self.screen_reader_mock).get_image_location(self.image_path_mock).thenRaise(ImageNotInScreenException)
        self.image_path_mock.file_name = 'image_path_mock'
        get_image_screen_region_use_case = StoreImageScreenRegionUseCase(
            container=self.container,
            max_tries=1,
            seconds_between_tries=0
        )

        with self.assertRaises(ImageNotInScreenException):
            get_image_screen_region_use_case.execute(self.image_path_mock, self.store_region)

    def test_execute_WHEN_image_not_found_THEN_try_again_as_many_times_as_defined(self) -> None:
        when(self.screen_reader_mock).get_image_location(self.image_path_mock).thenRaise(ImageNotInScreenException)
        get_image_screen_region_use_case = StoreImageScreenRegionUseCase(
            container=self.container,
            max_tries=2,
            seconds_between_tries=0
        )

        try:
            get_image_screen_region_use_case.execute(self.image_path_mock, self.store_region)
        except ImageNotInScreenException:
            pass

        verify(self.screen_reader_mock, times=2).get_image_location(self.image_path_mock)
