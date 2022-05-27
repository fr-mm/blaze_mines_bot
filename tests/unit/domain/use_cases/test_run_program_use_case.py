import time
from unittest import TestCase

from mockito import mock, unstub, when, verify

from domain.aggregates import Config
from domain.containers import RunProgramUseCaseContainer
from domain.ports import ClickerPort, TyperPort, KeyboardListenerPort, ScreenReaderPort, ConfigSetterInterfacePort, \
    GetImageScreenRegionUseCasePort
from domain.use_cases import RunProgramUseCase
from domain.value_objects import CheckForImageOnSquareMaxTries, ScreenRegion, ImagePath


class TestRunProgramUseCase(TestCase):
    def setUp(self) -> None:
        self.clicker_mock = mock(ClickerPort)
        self.typer_mock = mock(TyperPort)
        self.keyboard_listener_mock = mock(KeyboardListenerPort)
        self.screen_reader_mock = mock(ScreenReaderPort)
        self.config_setter_interface_mock = mock(ConfigSetterInterfacePort)
        self.get_image_screen_region_service_mock = mock(GetImageScreenRegionUseCasePort)
        self.check_for_image_on_square_max_tries = CheckForImageOnSquareMaxTries(1)

        self.container = RunProgramUseCaseContainer(
            clicker=self.clicker_mock,
            typer=self.typer_mock,
            keyboard_listener=self.keyboard_listener_mock,
            screen_reader=self.screen_reader_mock,
            config_setter_interface=self.config_setter_interface_mock,
            get_image_screen_region_service=self.get_image_screen_region_service_mock,
            check_for_image_on_square_max_tries=self.check_for_image_on_square_max_tries
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
        when(self.get_image_screen_region_service_mock).execute(...).thenReturn(self.screen_region_mock)
        when(time).sleep(...)

    def tearDown(self) -> None:
        unstub()

    def test_init_WHEN_called_THEN_returns_instance(self) -> None:
        RunProgramUseCase(self.container)

    def test_execute_WHEN_called_THEN_calls_config_setter_interface_prompt_user_config(self):
        run_program_use_case = RunProgramUseCase(self.container)

        run_program_use_case.execute(loop_forever=False)

        verify(self.container.config_setter_interface).prompt_user_config()
