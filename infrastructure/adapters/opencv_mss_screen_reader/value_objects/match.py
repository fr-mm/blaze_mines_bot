from dataclasses import dataclass

from infrastructure.adapters.opencv_mss_screen_reader.value_objects.match_location import MatchLocation
from infrastructure.adapters.opencv_mss_screen_reader.value_objects.match_size import MatchSize
from infrastructure.adapters.opencv_mss_screen_reader.value_objects.match_value import MatchValue


@dataclass(frozen=True)
class Match:
    value: MatchValue
    location: MatchLocation
    size: MatchSize
