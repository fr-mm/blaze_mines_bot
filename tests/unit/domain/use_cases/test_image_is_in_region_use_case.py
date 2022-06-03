from unittest import TestCase

from mockito import mock, when, verify

from domain.containers import ImageIsInRegionUseCaseContainer
from domain.entities import Image
from domain.ports import LocateImageInScreenUseCasePort, ScreenReaderPort
from domain.use_cases import ImageIsInRegionUseCase
from domain.value_objects import ScreenRegion


class TestImageIsInRegionUseCase(TestCase):
    def setUp(self) -> None:
        self.locate_image_in_screen_service = mock(LocateImageInScreenUseCasePort)
        self.screen_reader = mock(ScreenReaderPort)
        self.container = ImageIsInRegionUseCaseContainer(
            locate_image_in_screen_service=self.locate_image_in_screen_service,
            screen_reader=self.screen_reader
        )
        self.image = mock(Image)
        self.screen_region = mock(ScreenRegion)

    def test_execute_WHEN_screen_region_given_THEN_calls_screen_reader_image_is_in_region_with_given_image_and_region(self) -> None:
        when(self.screen_reader).image_is_in_region(
            image=self.image,
            screen_region=self.screen_region
        ).thenReturn(True)
        image_is_in_region_service = ImageIsInRegionUseCase(
            container=self.container
        )

        image_is_in_region_service.execute(
            image=self.image,
            screen_region=self.screen_region
        )

        verify(self.screen_reader).image_is_in_region(
            image=self.image,
            screen_region=self.screen_region
        )

    def test_execute_WHEN_screen_region_given_THEN_returns_screen_reader_image_is_in_region_result(self) -> None:
        when(self.screen_reader).image_is_in_region(
            image=self.image,
            screen_region=self.screen_region
        ).thenReturn(True)
        image_is_in_region_service = ImageIsInRegionUseCase(
            container=self.container
        )

        result = image_is_in_region_service.execute(
            image=self.image,
            screen_region=self.screen_region
        )

        self.assertTrue(result)

    def test_execute_WHEN_no_screen_region_given_THEN_calls_screen_region_image_is_in_region_with_image_location(self) -> None:
        self.image.region = self.screen_region
        when(self.screen_reader).image_is_in_region(
            image=self.image,
            screen_region=self.screen_region
        ).thenReturn(True)
        image_is_in_region_service = ImageIsInRegionUseCase(
            container=self.container
        )

        image_is_in_region_service.execute(
            image=self.image,
            screen_region=self.screen_region
        )

        verify(self.screen_reader).image_is_in_region(
            image=self.image,
            screen_region=self.screen_region
        )
