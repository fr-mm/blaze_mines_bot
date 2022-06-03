from typing import Callable

from domain.containers import ClickOnImageUseCaseContainer
from domain.ports import ClickOnImageUseCasePort
from domain.value_objects import ImagePath


class ClickOnImageUseCase(ClickOnImageUseCasePort):
    __container: ClickOnImageUseCaseContainer

    def __init__(self, container: ClickOnImageUseCaseContainer) -> None:
        self.__container = container

    def execute(self, image: ImagePath, store_region: Callable) -> None:
        pass
