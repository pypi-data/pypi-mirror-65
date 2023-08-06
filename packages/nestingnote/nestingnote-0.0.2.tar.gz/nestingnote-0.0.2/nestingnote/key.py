from enum import Enum, auto
import curses
from curses import ascii
import platform


class Key(Enum):
    ENTER = auto()
    BACKSPACE = auto()
    DELETE = auto()
    TAB = auto()
    SHIFT_TAB = auto()
    PAGE_UP = auto()
    PAGE_DOWN = auto()
    HOME = auto()
    END = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    CTRL_RIGHT = auto()
    CTRL_LEFT = auto()
    CTRL_K = auto()
    CTRL_W = auto()
    ESC = auto()


class KeyMap(object):
    """
    Ensures that keys are mapped to the right integer value given by curses.getch() independent of platform
    """
    __instance = None

    @staticmethod
    def get_instance():
        if KeyMap.__instance is None:
            KeyMap.__instance = KeyMap()
        return KeyMap.__instance

    def __init__(self):
        if KeyMap.__instance is not None:
            raise Exception("This class is a singleton")
        self.__map = self.__init_map()

    @staticmethod
    def __init_map() -> dict:
        key_map = {
            Key.ENTER: 10,
            Key.BACKSPACE: curses.KEY_BACKSPACE,
            Key.DELETE: curses.KEY_DC,
            Key.TAB: 9,
            Key.SHIFT_TAB: 353,
            Key.PAGE_UP: curses.KEY_PPAGE,
            Key.PAGE_DOWN: curses.KEY_NPAGE,
            Key.HOME: curses.KEY_HOME,
            Key.END: curses.KEY_END,
            Key.LEFT: curses.KEY_LEFT,
            Key.RIGHT: curses.KEY_RIGHT,
            Key.UP: curses.KEY_UP,
            Key.DOWN: curses.KEY_DOWN,
            Key.CTRL_RIGHT: 560,
            Key.CTRL_LEFT: 545,
            Key.CTRL_K: 11,
            Key.CTRL_W: 23,
            Key.ESC: curses.ascii.ESC
            }
        # Correct differences for windows
        if platform.system() == 'Windows':
            key_map[Key.BACKSPACE] = 8
            key_map[Key.SHIFT_TAB] = 351
        return key_map

    def value(self, key) -> int:
        try:
            return self.__map[key]
        except KeyError:
            raise Exception("{} not defined in key map".format(key))
