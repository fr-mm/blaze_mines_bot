import time

from domain.aggregates import Config
from domain.containers import RunProgramUseCaseContainer
from domain.entities import Image
from domain.enums import GameResultEnum
from domain.exceptions import UnexpectedGameResultException
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
        self.__set_starting_bet()

    def __main_loop(self) -> None:
        self.__container.printer.print_line(f'Iniciando loop {self.__turns}')
        self.__type_bet()
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

    def __type_bet(self) -> None:
        self.__container.printer.print_line('Digitando aposta')
        self.__container.click_on_image_service.execute(ImageSet.MONEY_SIGN)
        self.__container.typer.type_money(self.__current_bet)
        self.__sleep()

    def __set_starting_bet(self) -> None:
        self.__set_bet(money=self.__config.starting_bet)

    def __set_bet(self, money: Money) -> None:
        self.__container.printer.print_line(f'Configurando aposta: R${self.__current_bet}')
        self.__current_bet = money

    def __manage_game_result(self) -> None:
        self.__container.printer.print_line('Analizando resultado')
        game_result = self.__container.get_game_result_service.execute()
        if game_result == GameResultEnum.WIN:
            self.__manage_win()
        elif game_result == GameResultEnum.LOSS:
            self.__manage_loss()
        else:
            raise UnexpectedGameResultException()

    def __manage_win(self) -> None:
        self.__container.printer.print_line('Processando vitória')
        self.__click_on_withdraw_money()
        self.__profit.sum(self.__current_bet)
        self.__set_starting_bet()
        self.__wins += 1
        self.__turns += 1

    def __manage_loss(self) -> None:
        self.__container.printer.print_line('Processando derrota')
        if self.__current_martingale <= self.__config.max_martingales.value:
            self.__current_martingale += 1
            self.__container.printer.print_line(f'Aplicando {self.__current_martingale}° Martingale')
            self.__multiply_bet_by_martingale()
            self.__turns += 1
            self.__print_current_profit()
        else:
            self.__container.printer.print_line(f'Máximo de {self.__config.max_martingales.value} excedido. Reconfigurando aposta inicial')
            self.__current_martingale = 0
            self.__profit.subtract(self.__current_bet)
            self.__print_current_profit()
            self.__set_starting_bet()
            self.__losses += 1
            self.__turns += 1

    def __print_current_profit(self) -> None:
        if self.__profit.value < 0:
            absolute_profit = self.__profit.to_string().replace('-', '')
            formatted_profit = f'-R${absolute_profit}'
        else:
            formatted_profit = f'R#{self.__profit.to_string()}'
        self.__container.printer.print_line(f'Lucro atual: {formatted_profit}')

    def __multiply_bet_by_martingale(self) -> None:
        bet = self.__current_bet.multiply(self.__config.martingale_multiplier)
        self.__set_bet(bet)

    def __sleep(self) -> None:
        time.sleep(self.__config.seconds_between_actions.value)
