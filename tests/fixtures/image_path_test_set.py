from dataclasses import dataclass

from domain.value_objects import ImagePath


@dataclass(frozen=True)
class ImagePathTestSet:
    COMECAR_JOGO_NOT_FOUD = ImagePath('test_comecar_jogo_not_found.jpg')
    MONEY_SIGN_NOT_FOUND = ImagePath('test_money_sign_not_found.jpg')
    INITIAL_SCREEN = ImagePath('test_initial_screen.jpg')
    BOMB_AND_DIAMOND = ImagePath('test_bomb_and_diamond.jpg')
