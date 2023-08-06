from enum import IntEnum


class Direction(IntEnum):
    def __add__(self, other):
        return other + self.value
    '''
    Up = 1
    Down = -1
    Right = 1
    Left = -1
    '''


class VerticalDirection(Direction):
    UP = -1
    DOWN = 1


class LateralDirection(Direction):
    LEFT = -1
    RIGHT = 1
