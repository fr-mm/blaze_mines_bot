from domain.value_objects import Seconds, Money, MartingaleMultiplier, MaxMartingales


class Config:
    __seconds_between_actions: Seconds
    __starting_bet: Money
    __martingale_multiplier: MartingaleMultiplier
    __max_martingales: MaxMartingales
    __reset_after_max_martingales: bool

    def __init__(
            self,
            seconds_between_actions=1,
            starting_bet=5,
            martingale_multiplier=2.5,
            max_martingales=12,
            reset_after_max_martingales=True
    ) -> None:
        self.__seconds_between_actions = Seconds(seconds_between_actions)
        self.__starting_bet = Money(starting_bet)
        self.__martingale_multiplier = MartingaleMultiplier(martingale_multiplier)
        self.__max_martingales = MaxMartingales(max_martingales)
        self.__reset_after_max_martingales = reset_after_max_martingales

    @property
    def seconds_between_actions(self) -> Seconds:
        return self.__seconds_between_actions

    @property
    def starting_bet(self) -> Money:
        return self.__starting_bet

    @property
    def martingale_multiplier(self) -> MartingaleMultiplier:
        return self.__martingale_multiplier

    @property
    def max_martingales(self) -> MaxMartingales:
        return self.__max_martingales

    @property
    def reset_after_max_martingales(self) -> bool:
        return self.__reset_after_max_martingales

    @seconds_between_actions.setter
    def seconds_between_actions(self, value: float) -> None:
        self.__seconds_between_actions = Seconds(value)

    @starting_bet.setter
    def starting_bet(self, input_string: str) -> None:
        self.__starting_bet = Money.from_string(input_string)

    @martingale_multiplier.setter
    def martingale_multiplier(self, value: float) -> None:
        self.__martingale_multiplier = MartingaleMultiplier(value)

    @max_martingales.setter
    def max_martingales(self, value: int) -> None:
        self.__max_martingales = MaxMartingales(value)

    @reset_after_max_martingales.setter
    def reset_after_max_martingales(self, value: bool) -> None:
        self.__reset_after_max_martingales = value
