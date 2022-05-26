from abc import ABC, abstractmethod
from typing import Callable


class KeyboardListenerPort(ABC):
    @abstractmethod
    def set_callback_to_esc_key(self, callback: Callable) -> None:
        pass
