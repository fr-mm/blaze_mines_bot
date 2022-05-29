from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MatchLocation:
    min: Tuple[int, int]
    max: Tuple[int, int]
