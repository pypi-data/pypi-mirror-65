from nestingnote.styles import Styles
from nestingnote.view import View
from typing import List


class TestView(View):
    """
    Dummy View only used for testing model
    """

    def __init__(self, keys: List[int]):
        self.__inputs = keys
        self.__next = 0

    def get_size(self) -> (int, int):
        return 100, 100

    def addstr(self, y: int, x: int, string: str, style: Styles):
        pass

    def move_cursor(self, y: int, x: int):
        pass

    def clear(self):
        pass

    @property
    def input_char(self) -> int:
        next_key = self.__next
        self.__next += 1
        if next_key == len(self.__inputs):
            raise Exception("No more input")
        return self.__inputs[next_key]

    def signal_user_error(self):
        pass

    def refresh(self):
        pass
