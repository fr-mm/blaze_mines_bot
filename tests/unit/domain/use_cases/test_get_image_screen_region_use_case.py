import time
from unittest import TestCase

from mockito import mock, when, unstub, verify

from domain.containers import GetImageScreenRegionUseCaseContainer
from domain.exceptions import ImageNotInScreenException
from domain.ports import ScreenReaderPort, PrinterServicePort
from domain.use_cases import GetImageScreenRegionUseCase
from domain.value_objects import LocateImageMaxTries, ImagePath, ScreenRegion


class TestGetImageScreenRegionUseCase(TestCase):
    def setUp(self) -> None:
        self.screen_reader_mock = mock(ScreenReaderPort)
        self.image_path_mock = mock(ImagePath)
        self.screen_region_mock = mock(ScreenRegion)
        self.printer_mock = mock(PrinterServicePort)
        when(time).sleep(...)
        when(self.printer_mock).print(...)

    def tearDown(self) -> None:
        unstub()

    def test_execute_WHEN_image_found_THEN_returns_expected_screen_region(self) -> None:
        container = GetImageScreenRegionUseCaseContainer(
            screen_reader=self.screen_reader_mock,
            max_tries=LocateImageMaxTries(1),
            printer=self.printer_mock
        )
        when(self.screen_reader_mock).get_image_location(self.image_path_mock).thenReturn(self.screen_region_mock)
        get_image_screen_region_use_case = GetImageScreenRegionUseCase(container)

        result_screen_region = get_image_screen_region_use_case.execute(self.image_path_mock)

        expected_screen_region = self.screen_region_mock
        self.assertEqual(result_screen_region, expected_screen_region)

    def test_execute_WHEN_image_not_found_THEN_raises_image_not_in_screen_exception(self) -> None:
        container = GetImageScreenRegionUseCaseContainer(
            screen_reader=self.screen_reader_mock,
            max_tries=LocateImageMaxTries(1),
            printer=self.printer_mock
        )
        when(self.screen_reader_mock).get_image_location(self.image_path_mock).thenRaise(ImageNotInScreenException)
        self.image_path_mock.file_name = 'image_path_mock'
        get_image_screen_region_use_case = GetImageScreenRegionUseCase(container)

        with self.assertRaises(ImageNotInScreenException):
            get_image_screen_region_use_case.execute(self.image_path_mock)

    def test_execute_WHEN_image_not_found_THEN_try_again_as_many_times_as_defined(self) -> None:
        container = GetImageScreenRegionUseCaseContainer(
            screen_reader=self.screen_reader_mock,
            max_tries=LocateImageMaxTries(2),
            printer=self.printer_mock
        )
        when(self.screen_reader_mock).get_image_location(self.image_path_mock).thenRaise(ImageNotInScreenException)
        self.image_path_mock.file_name = 'image_path_mock'
        get_image_screen_region_use_case = GetImageScreenRegionUseCase(container)

        try:
            get_image_screen_region_use_case.execute(self.image_path_mock)
        except ImageNotInScreenException:
            pass

        verify(self.screen_reader_mock, times=2).get_image_location(self.image_path_mock)
