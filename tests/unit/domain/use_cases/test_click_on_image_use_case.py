from unittest import TestCase

from mockito import unstub, mock, when, verify

from domain.containers import ClickOnImageUseCaseContainer
from domain.entities import Image
from domain.ports import ClickerPort, LocateImageInScreenUseCasePort, ImageIsInRegionUseCasePort
from domain.use_cases import ClickOnImageUseCase
from domain.value_objects import ScreenRegion


class TestClickOnImageUseCase(TestCase):
    def setUp(self) -> None:
        self.clicker = mock(ClickerPort)
        self.locate_image_in_screen_service = mock(LocateImageInScreenUseCasePort)
        self.image_is_in_region_service = mock(ImageIsInRegionUseCasePort)
        self.container = ClickOnImageUseCaseContainer(
            clicker=self.clicker,
            locate_image_in_screen_service=self.locate_image_in_screen_service,
            image_is_in_region_service=self.image_is_in_region_service
        )
        self.image = mock(Image)

    def tearDown(self) -> None:
        unstub()

    def test_execute_WHEN_image_location_exists_THEN_calls_clicker_click_on_screen_region_with_given_image_location(self) -> None:
        self.image.location = mock(ScreenRegion)
        when(self.clicker).click_on_screen_region(self.image.location)
        when(self.locate_image_in_screen_service).execute(...)
        when(self.image_is_in_region_service).execute(...)
        click_on_image_service = ClickOnImageUseCase(
            container=self.container
        )

        click_on_image_service.execute(self.image)

        verify(self.clicker).click_on_screen_region(self.image.location)

    def test_execute_WHEN_image_location_exists_THEN_calls_image_is_in_region_use_case_execute_with_given_image(self) -> None:
        self.image.location = mock(ScreenRegion)
        when(self.clicker).click_on_screen_region(self.image.location)
        when(self.locate_image_in_screen_service).execute(...)
        when(self.image_is_in_region_service).execute(...)
        click_on_image_service = ClickOnImageUseCase(
            container=self.container
        )

        click_on_image_service.execute(self.image)

        verify(self.image_is_in_region_service).execute(self.image)

    def test_execute_WHEN_image_location_exists_but_not_in_region_THEN_calls_locate_image_in_screen_use_case_execute_with_given_image(self) -> None:
        self.image.location = mock(ScreenRegion)
        when(self.clicker).click_on_screen_region(self.image.location)
        when(self.locate_image_in_screen_service).execute(...)
        when(self.image_is_in_region_service).execute(...).thenReturn(False)
        click_on_image_service = ClickOnImageUseCase(
            container=self.container
        )

        click_on_image_service.execute(self.image)

        verify(self.locate_image_in_screen_service).execute(self.image)

    def test_execute_WHEN_image_location_does_not_exists_THEN_calls_locate_image_in_screen_use_case_with_given_image(self) -> None:
        self.image.location = None
        when(self.clicker).click_on_screen_region(self.image.location)
        when(self.locate_image_in_screen_service).execute(self.image)
        when(self.image_is_in_region_service).execute(...)
        click_on_image_service = ClickOnImageUseCase(
            container=self.container
        )

        click_on_image_service.execute(self.image)

        verify(self.locate_image_in_screen_service).execute(self.image)
