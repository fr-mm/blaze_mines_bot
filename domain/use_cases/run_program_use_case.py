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

    @property
    def profit(self) -> Profit:
        return self.__profit

    @profit.setter
    def profit(self, profit: Profit) -> None:
        self.__profit = profit

    @property
    def current_martingale(self) -> int:
        return self.__current_martingale

    @current_martingale.setter
    def current_martingale(self, current_martingale: int) -> None:
        self.__current_martingale = current_martingale

    @property
    def current_bet(self) -> Money:
        return self.__current_bet

    @current_bet.setter
    def current_bet(self, current_bet: Money) -> None:
        self.__current_bet = current_bet

    @property
    def wins(self) -> int:
        return self.__wins

    @wins.setter
    def wins(self, wins: int) -> None:
        self.__wins = wins

    @property
    def losses(self) -> int:
        return self.__losses

    @losses.setter
    def losses(self, losses: int) -> None:
        self.__losses = losses

    @property
    def turns(self) -> int:
        return self.__turns

    @turns.setter
    def turns(self, turns: int) -> None:
        self.__turns = turns

    @property
    def config(self) -> Config:
        return self.__config

    def execute(self, loop_forever: bool = True) -> None:
        self.__container.printer.print_line('Iniciando...')
        self.set_up()
        if loop_forever:
            while True:
                self.main_loop()
        else:
            self.main_loop()

    def set_up(self) -> None:
        self.prompt_user_config()
        self.set_starting_bet()

    def main_loop(self) -> None:
        self.__container.printer.print_line(f'Iniciando loop {self.__turns}')
        self.type_bet()
        self.click_on_start_game()
        self.click_on_square()
        self.manage_game_result()

    def prompt_user_config(self) -> None:
        self.__container.printer.print_line('Aguardando configurações')
        config = self.__container.config_setter_interface.prompt_user_config()
        if not config:
            quit()
        self.__config = config

    def click_on_start_game(self) -> None:
        self.click_on_image(ImageSet.START_GAME)

    def click_on_square(self) -> None:
        self.click_on_image(ImageSet.SQUARE)

    def click_on_money_sign(self) -> None:
        self.click_on_image(ImageSet.MONEY_SIGN)

    def click_on_withdraw_money(self) -> None:
        self.click_on_image(ImageSet.WITHDRAW_MONEY)

    def click_on_image(self, image: Image) -> None:
        self.__container.printer.print_line(f'Clicando em {image.name.value}')
        self.__container.click_on_image_service.execute(image)
        self.sleep()

    def type_bet(self) -> None:
        self.__container.printer.print_line('Digitando aposta')
        self.__container.click_on_image_service.execute(ImageSet.MONEY_SIGN)
        self.__container.typer.type_money(self.__current_bet)
        self.sleep()

    def set_starting_bet(self) -> None:
        self.set_bet(money=self.__config.starting_bet)

    def set_bet(self, money: Money) -> None:
        self.__container.printer.print_line(f'Configurando aposta: R${money.to_string()}')
        self.__current_bet = money

    def manage_game_result(self) -> None:
        self.__container.printer.print_line('Analizando resultado')
        game_result = self.__container.get_game_result_service.execute()
        if game_result == GameResultEnum.WIN:
            self.manage_win()
        elif game_result == GameResultEnum.LOSS:
            self.manage_loss()
        else:
            raise UnexpectedGameResultException()

    def manage_win(self) -> None:
        self.__container.printer.print_line('Processando vitória')
        self.click_on_withdraw_money()
        self.__profit.sum(self.__current_bet)
        self.set_starting_bet()
        self.__wins += 1
        self.__turns += 1

    def manage_loss(self) -> None:
        self.__container.printer.print_line('Processando derrota')
        if self.__current_martingale <= self.__config.max_martingales.value:
            self.apply_martingale_to_loss_result()
        else:
            self.manage_exceeded_martingale_loss()

    def apply_martingale_to_loss_result(self) -> None:
        self.__current_martingale += 1
        self.__container.printer.print_line(f'Aplicando {self.__current_martingale}° Martingale')
        self.__profit = self.__profit.subtract(self.__current_bet)
        self.multiply_bet_by_martingale()
        self.__turns += 1
        self.print_current_profit()

    def manage_exceeded_martingale_loss(self) -> None:
        self.__container.printer.print_line(
            f'Máximo de {self.__config.max_martingales.value} excedido. Reconfigurando aposta inicial')
        self.__current_martingale = 0
        self.__profit = self.__profit.subtract(self.__current_bet)
        self.print_current_profit()
        self.set_starting_bet()
        self.__losses += 1
        self.__turns += 1

    def print_current_profit(self) -> None:
        if self.__profit.value < 0:
            absolute_profit = self.__profit.to_string().replace('-', '')
            formatted_profit = f'-R${absolute_profit}'
        else:
            formatted_profit = f'R#{self.__profit.to_string()}'
        self.__container.printer.print_line(f'Lucro atual: {formatted_profit}')

    def multiply_bet_by_martingale(self) -> None:
        bet = self.__current_bet.multiply(self.__config.martingale_multiplier)
        self.set_bet(bet)

    def sleep(self) -> None:
        time.sleep(self.__config.seconds_between_actions.value)
