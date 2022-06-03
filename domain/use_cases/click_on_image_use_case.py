from typing import Callable

from domain.containers import ClickOnImageUseCaseContainer
from domain.entities import Image
from domain.ports import ClickOnImageUseCasePort


class ClickOnImageUseCase(ClickOnImageUseCasePort):
    __container: ClickOnImageUseCaseContainer

    def __init__(self, container: ClickOnImageUseCaseContainer) -> None:
        self.__container = container

    def execute(self, image: Image, store_region: Callable) -> None:
        pass
