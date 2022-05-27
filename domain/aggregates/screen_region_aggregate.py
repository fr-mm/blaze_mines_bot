from dataclasses import dataclass

from domain.value_objects import ScreenRegion


@dataclass
class ScreenRegionAggregate:
    start_game_or_withdraw_money: ScreenRegion = None
    bet: ScreenRegion = None
    square: ScreenRegion = None
