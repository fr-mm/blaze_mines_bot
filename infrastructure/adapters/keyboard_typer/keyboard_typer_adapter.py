import keyboard

from domain.ports import TyperPort
from domain.value_objects import Money


class KeyboardTyperAdapter(TyperPort):
    __seconds_between_keystrokes: float

    def __init__(self, seconds_between_keystrokes: float) -> None:
        self.__seconds_between_keystrokes = seconds_between_keystrokes

    def type_money(self, money: Money) -> None:
        for char in money.to_string():
            keyboard.write(
                text=char,
                delay=self.__seconds_between_keystrokes
            )
