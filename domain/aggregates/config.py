from dataclasses import dataclass

from domain.value_objects import Seconds, Money, MartingaleMultiplier, MaxMartingales


@dataclass(frozen=True)
class Config:
    seconds_between_actions: Seconds = Seconds(1)
    starting_bet: Money = Money(5)
    martingale_multiplier: MartingaleMultiplier = MartingaleMultiplier(2.5)
    max_martingales: MaxMartingales = MaxMartingales(12)
    reset_after_max_martingales: bool = True
