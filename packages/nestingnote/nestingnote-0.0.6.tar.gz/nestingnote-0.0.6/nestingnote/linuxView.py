import curses
from abc import ABC

from nestingnote.styles import Styles
from nestingnote.view import View


class LinuxView(View, ABC):

    def __init__(self, window):
        self.__window = window
        curses.init_pair(Styles.ODD, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(Styles.EVEN, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(Styles.HEADER, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(Styles.COLLAPSED_HEADER, curses.COLOR_WHITE, curses.COLOR_RED)

    @property
    def num_columns(self):
        rows, cols = self.__window.getmaxyx()
        return cols

    @property
    def num_rows(self):
        rows, cols = self.__window.getmaxyx()
        return rows

    def addstr(self, y: int, x: int, string: str, style: Styles):
        self.__window.addstr(y, x, string, curses.color_pair(style))

    def move_cursor(self, y: int, x: int):
        self.__window.move(y, x)

    def clear(self):
        self.__window.erase()

    @property
    def input_char(self) -> int:
        return self.__window.getch()

    def refresh(self):
        self.__window.refresh()

    def signal_user_error(self):
        curses.beep()

