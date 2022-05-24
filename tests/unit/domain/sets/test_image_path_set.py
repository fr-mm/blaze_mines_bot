from unittest import TestCase

from domain.sets import ImagePathSet


class TestImagePathSet(TestCase):
    def test_all_paths_are_valid(self) -> None:
        ImagePathSet()
