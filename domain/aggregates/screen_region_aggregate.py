from domain.value_objects import ScreenRegion


class ScreenRegionAggregate:
    __start_game: ScreenRegion or None
    __withdraw_money: ScreenRegion or None
    __bet_field: ScreenRegion or None
    __square: ScreenRegion or None

    def __init__(self) -> None:
        self.__start_game = None
        self.__withdraw_money = None
        self.__bet_field = None
        self.__square = None

    @property
    def start_game(self) -> ScreenRegion:
        return self.__start_game

    @property
    def withdraw_money(self) -> ScreenRegion:
        return self.__withdraw_money

    @property
    def bet_field(self) -> None:
        return self.__bet_field

    @property
    def square(self) -> None:
        return self.__square

    def set_start_game(self, screen_region: ScreenRegion) -> None:
        self.__start_game = screen_region

    def set_withdraw_money(self, screen_region: ScreenRegion) -> None:
        self.__withdraw_money = screen_region

    def set_bet_field(self, screen_region: ScreenRegion) -> None:
        self.__bet_field = screen_region

    def set_square(self, screen_region: ScreenRegion) -> None:
        self.__square = screen_region
