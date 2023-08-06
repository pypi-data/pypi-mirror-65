from nestingnote.model import Model
from nestingnote.directions import VerticalDirection, LateralDirection
from abc import abstractmethod, ABC
from nestingnote.key import KeyMap, Key
import sys


class KeyCommand(ABC):

    @property
    def key_map(self):
        return KeyMap.get_instance()

    @abstractmethod
    def is_relevant(self, key: int, model: Model):
        pass

    @abstractmethod
    def execute(self, key: int, model: Model):
        pass


class NewLine(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.ENTER)

    def execute(self, key: int, model: Model):
        model.split_node()


class BackspaceNewline(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return model.get_level() == 0 and key == self.key_map.value(Key.BACKSPACE) and model.at_line_start() and not model.at_root()

    def execute(self, key: int, model: Model):
        model.combine_nodes()


class IndentTab(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.TAB) and model.at_line_start() and not model.is_first_child()

    def execute(self, key: int, model: Model):
        model.indent_current_node()


class SplitTab(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.TAB) and not model.at_line_start()

    def execute(self, key: int, model: Model):
        model.split_field()


class UnIndent(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return not model.at_root() and (key == self.key_map.value(Key.BACKSPACE) and model.at_line_start()) \
               or key == self.key_map.value(Key.SHIFT_TAB)

    def execute(self, key: int, model: Model):
        model.unindent_current_node()


class UnSplitBackspace(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.BACKSPACE) and not model.at_line_start() and model.at_field_end(LateralDirection.LEFT)

    def execute(self, key: int, model: Model):
        model.combine_fields(LateralDirection.LEFT)


class UnSplitDelete(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.DELETE) and not model.at_line_end() \
               and model.at_field_end(LateralDirection.RIGHT)

    def execute(self, key: int, model: Model):
        model.combine_fields(LateralDirection.RIGHT)


class Insert(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return 31 < key < 127  # printable char ascii range

    def execute(self, key: int, model: Model):
        model.insert(chr(key))


class TextBackspace(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.BACKSPACE) and not model.at_field_end(LateralDirection.LEFT)

    def execute(self, key: int, model: Model):
        model.delete(-1)


class TextDelete(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.DELETE) and not model.at_field_end(LateralDirection.RIGHT)

    def execute(self, key: int, model: Model):
        model.delete(0)


class PageUp(KeyCommand):
    def is_relevant(self, key: int, model: Model) -> bool:
        return key == self.key_map.value(Key.PAGE_UP)

    def execute(self, key, model: Model):
        model.page(VerticalDirection.UP)


class Home(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.HOME)

    def execute(self, key: int, model: Model):
        model.move_end(LateralDirection.LEFT)


class End(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.END)

    def execute(self, key: int, model: Model):
        model.move_end(LateralDirection.RIGHT)


class PageDn(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.PAGE_DOWN)

    def execute(self, key: int, model: Model):
        model.page(VerticalDirection.DOWN)


class Up(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.UP)

    def execute(self, key: int, model: Model):
        model.move(VerticalDirection.UP)


class Left(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.LEFT)

    def execute(self, key: int, model: Model):
        model.move(LateralDirection.LEFT)


class Right(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.RIGHT)

    def execute(self, key: int, model: Model):
        padding_len: int = model.get_padding_len()
        if model.at_field_end(LateralDirection.RIGHT):
            num_spaces = padding_len
        else:
            num_spaces = 1
        model.move(LateralDirection.RIGHT, num_spaces)


class CtrLeft(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.CTRL_LEFT)

    def execute(self, key: int, model: Model):
        left = LateralDirection.LEFT
        if model.at_field_end(left):
            model.move(left, model.get_neighbor_column_width(left))
        else:
            model.move_field_end(left)


class CtrRight(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.CTRL_RIGHT) and not model.at_line_end()

    def execute(self, key: int, model: Model):
        right = LateralDirection.RIGHT
        if model.at_field_end(right):
            model.move(right, model.get_padding_len() + len(model.get_neighbor_field(right)))
        else:
            model.move_field_end(right)


class Down(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.DOWN)

    def execute(self, key: int, model: Model):
        model.move(VerticalDirection.DOWN)


class Esc(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.ESC)

    def execute(self, key: int, model: Model):
        sys.exit()


class ToggleCollapse(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return model.current_node_has_child and key == self.key_map.value(Key.CTRL_K) or \
               (key == self.key_map.value(Key.ENTER) and model.collapsed)

    def execute(self, key: int, model: Model):
        model.toggle_current_node_collapsed()


class Save(KeyCommand):
    def is_relevant(self, key: int, model: Model):
        return key == self.key_map.value(Key.CTRL_W)

    def execute(self, key: int, model: Model):
        model.save()


class UserError(KeyCommand):
    """
    Precondition: All other KeyCommand subclasses are checked (is_relevant()) before this is run
    This must remain the last subclass of KeyCommand
    listed below the others in this file.
    """

    def is_relevant(self, key: int, model: Model):
        return True

    def execute(self, key: int, model: Model):
        model.signal_user_error()


class Commands(object):
    # contains all subclasses oh KeyCommand
    __key_commands = []

    @classmethod
    def __get_key_commands(cls):
        if len(cls.__key_commands) == 0:
            for subclass in KeyCommand.__subclasses__():
                cls.__key_commands.append(subclass())
        return cls.__key_commands

    @classmethod
    def __get_command(cls, key: int, model: Model) -> KeyCommand:
        for command in Commands.__get_key_commands():
            if command.is_relevant(key, model):
                return command
        raise Exception("No relevant command")

    @classmethod
    def execute(cls, key: int, model: Model):
        command = Commands.__get_command(key, model)
        command.execute(key, model)
