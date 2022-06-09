import time
from unittest import TestCase

from mockito import mock, unstub, when, verify

from domain.aggregates import Config
from domain.containers import RunProgramUseCaseContainer
from domain.entities import Image
from domain.enums import GameResultEnum
from domain.services import PrinterService
from domain.ports import ClickerPort, TyperPort, KeyboardListenerPort, ScreenReaderPort, ConfigSetterInterfacePort, \
    LocateImageInScreenUseCasePort, GetGameResultUseCasePort
from domain.sets.image_set import ImageSet
from domain.use_cases import RunProgramUseCase, ClickOnImageUseCase
from domain.value_objects import ScreenRegion, ImagePath, Seconds, Money, Profit, MartingaleMultiplier


class TestRunProgramUseCase(TestCase):
    def setUp(self) -> None:
        self.screen_region_mock = mock(ScreenRegion)
        self.image_path_mock = mock(ImagePath)
        self.config = Config()
        self.clicker_mock = mock(ClickerPort)
        self.typer_mock = mock(TyperPort)
        self.keyboard_listener_mock = mock(KeyboardListenerPort)
        self.screen_reader_mock = mock(ScreenReaderPort)
        self.config_setter_interface_mock = mock(ConfigSetterInterfacePort)
        self.locate_image_in_screen_service_mock = mock(LocateImageInScreenUseCasePort)
        self.printer_mock = mock(PrinterService)
        self.click_on_image_service = mock(ClickOnImageUseCase)
        self.get_game_result_service = mock(GetGameResultUseCasePort)

        when(self.printer_mock).print_line(...)
        when(self.printer_mock).print_open_line(...)
        when(self.printer_mock).close_line()
        when(RunProgramUseCase).sleep()

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
        self.events = []

    def tearDown(self) -> None:
        unstub()
        self.reset_images_locations()
        self.events = []

    @staticmethod
    def reset_images_locations() -> None:
        ImageSet.SQUARE.location = None
        ImageSet.DIAMOND.location = None
        ImageSet.BOMB.location = None
        ImageSet.START_GAME.location = None
        ImageSet.MONEY_SIGN.location = None
        ImageSet.WITHDRAW_MONEY.location = None

    def record_event(self, event: str) -> None:
        self.events.append(event)

    def test_init_WHEN_called_THEN_returns_instance(self) -> None:
        RunProgramUseCase(container=self.container)

    def test_execute_WHEN_called_THEN_calls_set_up_before_calling_main_loop(self) -> None:
        set_up_event = 'SET UP'
        main_loop_event = 'MAIN LOOP'
        when(RunProgramUseCase).set_up().thenReturn(self.record_event(set_up_event))
        when(RunProgramUseCase).main_loop().thenReturn(self.record_event(main_loop_event))
        run_program_service = RunProgramUseCase(container=self.container)

        run_program_service.execute(loop_forever=False)

        expected_event_order = [set_up_event, main_loop_event]
        self.assertEqual(self.events, expected_event_order)

    def test_set_up_WHEN_called_THEN_calls_prompt_user_config_and_then_set_starting_bet(self) -> None:
        prompt_user_config_event = 'PROMPT USER CONFIG'
        set_starting_bet_event = 'SET STARTING BET'
        when(RunProgramUseCase).prompt_user_config().thenReturn(self.record_event(prompt_user_config_event))
        when(RunProgramUseCase).set_starting_bet().thenReturn(self.record_event(set_starting_bet_event))
        when(RunProgramUseCase).main_loop()
        run_program_service = RunProgramUseCase(container=self.container)

        run_program_service.execute(loop_forever=False)

        expected_event_order = [prompt_user_config_event, set_starting_bet_event]
        self.assertEqual(self.events, expected_event_order)

    def test_main_loop_WHEN_called_THEN_calls_expected_methods_in_order(self) -> None:
        type_bet_event = 'TYPE_BET'
        click_on_start_game_event = 'CLICK ON START GAME'
        click_on_square_event = 'CLICK ON SQUARE EVENT'
        manage_game_result_event = 'MANAGE GAME RESULT'
        when(RunProgramUseCase).type_bet().thenReturn(self.record_event(type_bet_event))
        when(RunProgramUseCase).click_on_start_game().thenReturn(self.record_event(click_on_start_game_event))
        when(RunProgramUseCase).click_on_square().thenReturn(self.record_event(click_on_square_event))
        when(RunProgramUseCase).manage_game_result().thenReturn(self.record_event(manage_game_result_event))
        when(self.config_setter_interface_mock).prompt_user_config().thenReturn(self.config)
        run_program_service = RunProgramUseCase(container=self.container)

        run_program_service.execute(loop_forever=False)

        expected_event_order = [
            type_bet_event,
            click_on_start_game_event,
            click_on_square_event,
            manage_game_result_event
        ]
        self.assertEqual(self.events, expected_event_order)

    def test_prompt_user_config_WHEN_called_THEN_assigns_config_setter_interface_return_to_config(self) -> None:
        when(self.config_setter_interface_mock).prompt_user_config().thenReturn(self.config)
        run_program_interface = RunProgramUseCase(container=self.container)

        run_program_interface.prompt_user_config()

        self.assertEqual(run_program_interface.config, self.config)

    def test_click_on_image_WHEN_image_given_THEN_calls_click_on_image_service_execute_with_given_image(self) -> None:
        image = ImageSet.BOMB
        when(self.click_on_image_service).execute(image)
        run_program_service = RunProgramUseCase(container=self.container)

        run_program_service.click_on_image(image)

        verify(self.click_on_image_service).execute(image)

    def test_type_bet_WHEN_current_bet_is_set_THEN_calls_typer_type_money_with_current_bet(self) -> None:
        current_bet = Money(100)
        when(self.click_on_image_service).execute(ImageSet.MONEY_SIGN)
        when(self.typer_mock).type_money(current_bet)
        run_program_interface = RunProgramUseCase(container=self.container)
        run_program_interface.set_bet(current_bet)

        run_program_interface.type_bet()

        verify(self.typer_mock).type_money(current_bet)

    def test_manage_game_result_WHEN_result_is_win_THEN_calls_manage_win(self) -> None:
        when(self.get_game_result_service).execute().thenReturn(GameResultEnum.WIN)
        when(RunProgramUseCase).manage_win()
        run_program_service = RunProgramUseCase(container=self.container)

        run_program_service.manage_game_result()

        verify(RunProgramUseCase).manage_win()

    def test_manage_game_result_WHEN_result_is_loss_THEN_calls_manage_loss(self) -> None:
        when(self.get_game_result_service).execute().thenReturn(GameResultEnum.LOSS)
        when(RunProgramUseCase).manage_loss()
        run_program_service = RunProgramUseCase(container=self.container)

        run_program_service.manage_game_result()

        verify(RunProgramUseCase).manage_loss()

    def test_apply_martingale_to_loss_result_WHEN_called_THEN_increments_current_martingale(self) -> None:
        when(RunProgramUseCase).multiply_bet_by_martingale()
        when(RunProgramUseCase).print_current_profit()
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.current_martingale = 3
        run_program_service.current_bet = Money(100)

        run_program_service.apply_martingale_to_loss_result()

        expected_current_martingale = 4
        self.assertEqual(run_program_service.current_martingale, expected_current_martingale)

    def test_apply_martingale_to_loss_result_WHEN_called_THEN_calls_multiply_bet_by_martingale(self) -> None:
        when(RunProgramUseCase).multiply_bet_by_martingale()
        when(RunProgramUseCase).print_current_profit()
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.current_bet = Money(100)

        run_program_service.apply_martingale_to_loss_result()

        verify(RunProgramUseCase).multiply_bet_by_martingale()

    def test_apply_martingale_to_loss_result_WHEN_called_THEN_increments_turns(self) -> None:
        when(RunProgramUseCase).multiply_bet_by_martingale()
        when(RunProgramUseCase).print_current_profit()
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.turns = 3
        run_program_service.current_bet = Money(100)

        run_program_service.apply_martingale_to_loss_result()

        expected_turns = 4
        self.assertEqual(run_program_service.turns, expected_turns)

    def test_apply_martingale_to_loss_result_WHEN_has_profit_THEN_subtracts_bet_from_profit(self) -> None:
        when(RunProgramUseCase).multiply_bet_by_martingale()
        when(RunProgramUseCase).print_current_profit()
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.profit = Profit(300)
        run_program_service.current_bet = Money(100)

        run_program_service.apply_martingale_to_loss_result()

        expected_profit = Profit(200)
        self.assertEqual(run_program_service.profit, expected_profit)

    def test_manage_exceeded_martingale_loss_WHEN_called_THEN_resets_current_martingale(self) -> None:
        when(RunProgramUseCase).multiply_bet_by_martingale()
        when(RunProgramUseCase).print_current_profit()
        when(RunProgramUseCase).set_starting_bet()
        when(self.config_setter_interface_mock).prompt_user_config().thenReturn(self.config)
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.prompt_user_config()
        run_program_service.current_bet = Money(100)
        run_program_service.current_martingale = 8

        run_program_service.manage_exceeded_martingale_loss()

        expected_current_martingale = 0
        self.assertEqual(run_program_service.current_martingale, expected_current_martingale)

    def test_manage_exceeded_martingale_loss_WHEN_has_profit_THEN_subtracts_bet_from_profit(self) -> None:
        when(RunProgramUseCase).multiply_bet_by_martingale()
        when(RunProgramUseCase).print_current_profit()
        when(RunProgramUseCase).set_starting_bet()
        when(self.config_setter_interface_mock).prompt_user_config().thenReturn(self.config)
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.prompt_user_config()
        run_program_service.profit = Profit(300)
        run_program_service.current_bet = Money(100)

        run_program_service.manage_exceeded_martingale_loss()

        expected_profit = Profit(200)
        self.assertEqual(run_program_service.profit, expected_profit)

    def test_manage_exceeded_martingale_loss_WHEN_called_THEN_calls_set_starting_bet(self) -> None:
        when(RunProgramUseCase).multiply_bet_by_martingale()
        when(RunProgramUseCase).print_current_profit()
        when(RunProgramUseCase).set_starting_bet()
        when(self.config_setter_interface_mock).prompt_user_config().thenReturn(self.config)
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.prompt_user_config()
        run_program_service.current_bet = Money(100)

        run_program_service.manage_exceeded_martingale_loss()

        verify(RunProgramUseCase).set_starting_bet()

    def test_manage_exceeded_martingale_loss_WHEN_called_THEN_increments_losses(self) -> None:
        when(RunProgramUseCase).multiply_bet_by_martingale()
        when(RunProgramUseCase).print_current_profit()
        when(RunProgramUseCase).set_starting_bet()
        when(self.config_setter_interface_mock).prompt_user_config().thenReturn(self.config)
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.prompt_user_config()
        run_program_service.current_bet = Money(100)
        run_program_service.losses = 8

        run_program_service.manage_exceeded_martingale_loss()

        expected_losses = 9
        self.assertEqual(run_program_service.losses, expected_losses)

    def test_manage_exceeded_martingale_loss_WHEN_called_THEN_increments_turns(self) -> None:
        when(RunProgramUseCase).multiply_bet_by_martingale()
        when(RunProgramUseCase).print_current_profit()
        when(RunProgramUseCase).set_starting_bet()
        when(self.config_setter_interface_mock).prompt_user_config().thenReturn(self.config)
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.prompt_user_config()
        run_program_service.current_bet = Money(100)
        run_program_service.turns = 8

        run_program_service.manage_exceeded_martingale_loss()

        expected_turns = 9
        self.assertEqual(run_program_service.turns, expected_turns)

    def test_multiply_bet_by_martingale_WHEN_bet_is_set_THEN_multiplies_it_by_martingale_multiplier(self) -> None:
        config = Config(martingale_multiplier=MartingaleMultiplier(3))
        when(self.config_setter_interface_mock).prompt_user_config().thenReturn(config)
        run_program_service = RunProgramUseCase(container=self.container)
        run_program_service.prompt_user_config()
        previous_bet = Money(100)
        run_program_service.current_bet = previous_bet

        run_program_service.multiply_bet_by_martingale()

        expected_bet = Money(300)
        self.assertEqual(run_program_service.current_bet, expected_bet)
