import time

from domain.aggregates import ScreenRegionAggregate, Config
from domain.containers import RunProgramUseCaseContainer
from domain.exceptions import QuitProgramKeyPressedException
from domain.ports import RunProgramUseCasePort
from domain.sets import ImagePathSet
from domain.value_objects import Money, Profit, ImagePath


class RunProgramUseCase(RunProgramUseCasePort):
    __container: RunProgramUseCaseContainer
    __current_bet: Money
    __screen_regions: ScreenRegionAggregate
    __profit: Profit
    __config: Config
    __current_martingale: int
    __image_location_error: bool
    __wins: int
    __losses: int
    __turns: int

    def __init__(self, container: RunProgramUseCaseContainer) -> None:
        self.__container = container
        self.__screen_regions = ScreenRegionAggregate()
        self.__profit = Profit(0)
        self.__image_location_error = False
        self.__wins = 0
        self.__losses = 0
        self.__turns = 0

    def execute(self, loop_forever: bool = True) -> None:
        self.__set_up()
        try:
            if loop_forever:
                while True:
                    self.__main_loop()
            else:
                self.__main_loop()
        except QuitProgramKeyPressedException:
            pass

    def __main_loop(self) -> None:
        self.__click_on_start_game_or_withdraw_money_button()
        self.__click_on_square()
        self.__manage_game_result()
        self.__reset_image_location_error()

    def __set_up(self) -> None:
        self.__config = self.__container.config_setter_interface.prompt_user_config()
        self.__listen_for_quit_program_key()
        self.__store_images_locations()
        self.__set_starting_bet()

    def __store_images_locations(self) -> None:
        self.__locate_start_game_button()
        self.__locate_bet_field()
        self.__locate_square()

    def __locate_start_game_button(self) -> None:
        location = self.__container.get_image_screen_region_service.execute(ImagePathSet.COMECAR_JOGO)
        self.__screen_regions.start_game_or_withdraw_money = location

    def __locate_bet_field(self) -> None:
        location = self.__container.get_image_screen_region_service.execute(ImagePathSet.MONEY_SIGN)
        self.__screen_regions.bet = location

    def __locate_square(self) -> None:
        location = self.__container.get_image_screen_region_service.execute(ImagePathSet.SQUARE)
        self.__screen_regions.square = location

    def __set_starting_bet(self) -> None:
        self.__set_bet(self.__config.starting_bet)

    def __set_bet(self, money: Money) -> None:
        self.__relocate_bet_field_when_image_location_error()
        self.__container.clicker.click_on_screen_region(self.__screen_regions.bet)
        self.__container.typer.type_money(money)
        self.__current_bet = money
        self.__sleep()

    def __click_on_square(self) -> None:
        self.__container.clicker.click_on_screen_region(self.__screen_regions.square)
        self.__sleep()

    def __diamond_appeared(self) -> bool:
        return self.__image_appeared_on_square(ImagePathSet.DIAMOND)

    def __bomb_appeared(self) -> bool:
        return self.__image_appeared_on_square(ImagePathSet.BOMB)

    def __image_appeared_on_square(self, image_path: ImagePath) -> bool:
        return self.__container.screen_reader.image_is_in_region(
            image_path=image_path,
            screen_region=self.__screen_regions.square
        )

    def __manage_game_result(self) -> None:
        for _ in range(self.__container.check_for_image_on_square_max_tries.value):
            if self.__diamond_appeared():
                self.__manage_win()
            elif self.__bomb_appeared():
                self.__manage_loss()
            else:
                self.__image_location_error = True
                self.__sleep()
                self.__locate_square()

    def __manage_win(self) -> None:
        self.__click_on_start_game_or_withdraw_money_button()
        self.__profit.sum(self.__current_bet)
        self.__set_starting_bet()
        self.__wins += 1
        self.__turns += 1

    def __manage_loss(self) -> None:
        if self.__current_martingale <= self.__config.max_martingales.value:
            self.__current_martingale += 1
            self.__multiply_bet_by_martingale()
            self.__turns += 1
        else:
            self.__current_martingale = 0
            self.__profit.subtract(self.__current_bet)
            self.__set_starting_bet()
            self.__losses += 1
            self.__turns += 1

    def __multiply_bet_by_martingale(self) -> None:
        bet = self.__current_bet.multiply(self.__config.martingale_multiplier)
        self.__set_bet(bet)

    def __relocate_start_game_button_when_image_location_error(self) -> None:
        if self.__image_location_error:
            self.__locate_start_game_button()

    def __relocate_bet_field_when_image_location_error(self) -> None:
        if self.__image_location_error:
            self.__locate_bet_field()

    def __click_on_start_game_or_withdraw_money_button(self) -> None:
        self.__relocate_start_game_button_when_image_location_error()
        self.__container.clicker.click_on_screen_region(self.__screen_regions.start_game_or_withdraw_money)
        self.__sleep()

    def __reset_image_location_error(self) -> None:
        self.__image_location_error = False

    def __sleep(self) -> None:
        time.sleep(self.__config.seconds_between_actions.value)

    def __listen_for_quit_program_key(self) -> None:
        self.__container.keyboard_listener.set_callback_to_esc_key(self.__quit_program)

    def __quit_program(self) -> None:
        raise QuitProgramKeyPressedException(
            'Quitting program'
        )
