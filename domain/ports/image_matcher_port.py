from abc import ABC, abstractmethod


class ImageMatcherPort(ABC):
    @abstractmethod
    def match_in_screen_region(self, ):
