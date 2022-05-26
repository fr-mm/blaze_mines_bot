from typing import Callable

import keyboard

from domain.ports import KeyboardListenerPort


class KeyboardKeyboardListenerAdapter(KeyboardListenerPort):
    def set_callback_to_esc_key(self, callback: Callable) -> None:
        keyboard.add_hotkey(
            hotkey='esc',
            callback=callback
        )
