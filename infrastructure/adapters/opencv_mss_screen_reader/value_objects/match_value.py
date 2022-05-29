from dataclasses import dataclass


@dataclass(frozen=True)
class MatchValue:
    min: float
    max: float
