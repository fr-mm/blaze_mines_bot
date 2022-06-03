from unittest import TestCase

from domain.sets.image_set import ImageSet


class TestImagePathSet(TestCase):
    def test_all_paths_are_valid(self) -> None:
        ImageSet()
