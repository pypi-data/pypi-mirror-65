from nestingnote.styles import Styles
from abc import ABC, abstractmethod


class View(ABC):

    @abstractmethod
    def signal_user_error(self):
        pass

    @property
    @abstractmethod
    def num_columns(self):
        pass

    @property
    @abstractmethod
    def num_rows(self):
        pass

    @abstractmethod
    def addstr(self, y: int, x: int, string: str, style: Styles):
        pass

    @abstractmethod
    def move_cursor(self, y: int, x: int):
        pass

    @abstractmethod
    def clear(self):
        pass

    @property
    @abstractmethod
    def input_char(self) -> int:
        pass

    @abstractmethod
    def refresh(self):
        pass

