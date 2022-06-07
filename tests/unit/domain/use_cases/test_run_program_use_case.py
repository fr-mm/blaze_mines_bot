import time
from unittest import TestCase

from mockito import mock, unstub, when

from domain.aggregates import Config
from domain.containers import RunProgramUseCaseContainer
from domain.services import PrinterService
from domain.ports import ClickerPort, TyperPort, KeyboardListenerPort, ScreenReaderPort, ConfigSetterInterfacePort, \
    LocateImageInScreenUseCasePort, GetGameResultUseCasePort
from domain.use_cases import RunProgramUseCase, ClickOnImageUseCase
from domain.value_objects import ScreenRegion, ImagePath


class TestRunProgramUseCase(TestCase):
    def setUp(self) -> None:
        self.clicker_mock = mock(ClickerPort)
        self.typer_mock = mock(TyperPort)
        self.keyboard_listener_mock = mock(KeyboardListenerPort)
        self.screen_reader_mock = mock(ScreenReaderPort)
        self.config_setter_interface_mock = mock(ConfigSetterInterfacePort)
        self.locate_image_in_screen_service_mock = mock(LocateImageInScreenUseCasePort)
        self.printer_mock = mock(PrinterService)
        self.click_on_image_service = mock(ClickOnImageUseCase)
        self.get_game_result_service = mock(GetGameResultUseCasePort)

        self.container = RunProgramUseCaseContainer(
            clicker=self.clicker_mock,
            typer=self.typer_mock,
            keyboard_listener=self.keyboard_listener_mock,
            screen_reader=self.screen_reader_mock,
            config_setter_interface=self.config_setter_interface_mock,
            locate_image_in_screen_service=self.locate_image_in_screen_service_mock,
            printer=self.printer_mock,
            click_on_image_service=self.click_on_image_service,
            get_game_result_service=self.get_game_result_service
        )

        self.screen_region_mock = mock(ScreenRegion)
        self.image_path_mock = mock(ImagePath)
        self.config = Config()

        when(self.clicker_mock).click_on_screen_region(...)
        when(self.typer_mock).type_money(...)
        when(self.keyboard_listener_mock).set_callback_to_esc_key(...)
        when(self.screen_reader_mock).get_image_location(...).thenReturn(self.screen_region_mock)
        when(self.screen_reader_mock).image_is_in_region(..., ...).thenReturn(True)
        when(self.config_setter_interface_mock).prompt_user_config().thenReturn(self.config)
        when(self.locate_image_in_screen_service_mock).execute(...)
        when(self.printer_mock).print_line(...)
        when(self.click_on_image_service).execute(...)
        when(time).sleep(...)

    def tearDown(self) -> None:
        unstub()

    def test_init_WHEN_called_THEN_returns_instance(self) -> None:
        RunProgramUseCase(self.container)
