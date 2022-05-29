from dataclasses import dataclass


@dataclass(frozen=True)
class MatchSize:
    width: int
    height: int
