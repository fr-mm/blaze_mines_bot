import time

from domain.aggregates import Config
from domain.containers import RunProgramUseCaseContainer
from domain.entities import Image
from domain.ports import RunProgramUseCasePort
from domain.sets.image_set import ImageSet
from domain.value_objects import Money, Profit


class RunProgramUseCase(RunProgramUseCasePort):
    __container: RunProgramUseCaseContainer
    __current_bet: Money
    __profit: Profit
    __config: Config
    __current_martingale: int
    __image_location_error: bool
    __wins: int
    __losses: int
    __turns: int

    def __init__(self, container: RunProgramUseCaseContainer) -> None:
        self.__container = container
        self.__profit = Profit(0)
        self.__current_martingale = 0
        self.__wins = 0
        self.__losses = 0
        self.__turns = 0

    def execute(self, loop_forever: bool = True) -> None:
        self.__container.printer.print_line('Iniciando...')
        self.__set_up()
        if loop_forever:
            while True:
                self.__main_loop()
        else:
            self.__main_loop()

    def __set_up(self) -> None:
        self.__prompt_user_config()
        self.__current_bet = self.__config.starting_bet

    def __main_loop(self) -> None:
        self.__container.printer.print_line(f'Iniciando loop {self.__turns}')
        self.__click_on_start_game()
        self.__click_on_square()
        self.__manage_game_result()

    def __prompt_user_config(self) -> None:
        self.__container.printer.print_line('Aguardando configurações')
        config = self.__container.config_setter_interface.prompt_user_config()
        if not config:
            quit()
        self.__config = config

    def __click_on_start_game(self) -> None:
        self.__click_on_image(ImageSet.START_GAME)

    def __click_on_square(self) -> None:
        self.__click_on_image(ImageSet.SQUARE)

    def __click_on_money_sign(self) -> None:
        self.__click_on_image(ImageSet.MONEY_SIGN)

    def __click_on_withdraw_money(self) -> None:
        self.__click_on_image(ImageSet.WITHDRAW_MONEY)

    def __click_on_image(self, image: Image) -> None:
        self.__container.printer.print_line(f'Clicando em {image.name.value}')
        self.__container.click_on_image_service.execute(image)
        self.__sleep()

    def __type_bet(self, money: Money) -> None:
        self.__container.printer.print_line('Digitando aposta')
        self.__container.click_on_image_service.execute(ImageSet.MONEY_SIGN)
        self.__container.typer.type_money(money)
        self.__sleep()

    def __set_bet(self, money: Money) -> None:
        self.__container.printer.print_line(f'Configurando aposta: R${self.__current_bet}')
        self.__current_bet = money

    def __diamond_appeared(self) -> bool:
        return self.__image_appeared_on_square(ImageSet.DIAMOND.location)

    def __bomb_appeared(self) -> bool:
        return self.__image_appeared_on_square(ImageSet.BOMB.location)

    def __image_appeared_on_square(self, image: Image) -> bool:
        return self.__container.screen_reader.image_is_in_region(
            image=image,
            screen_region=ImageSet.SQUARE.location
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
        self.__click_on_withdraw_money()
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
        self.__type_bet(bet)

    def __sleep(self) -> None:
        time.sleep(self.__config.seconds_between_actions.value)
