from nestingnote.directions import VerticalDirection, LateralDirection, Direction
from nestingnote.view import View
from nestingnote.styles import Styles
from nestingnote.nestedlist import NestedList, NullNestedList
import json
import os.path


class Model(object):

    __tab: str = "    "

    __file_extension = '.nnn'

    def __init__(self, view: View, file_path: str = None, root: NestedList = None):
        """
        Attributes
            max_lines: Maximum visible line count for `result_window`
            __top: Available __top line position for current page (used on scrolling)
            __num_lines(): Available __num_lines() line position for whole pages (as length of items)
            current: Current highlighted line number (as window cursor)
            page: Total page count which being changed corresponding to result of a query (starts from 0)
            ┌--------------------------------------┐
            |1. Item                               |
            |--------------------------------------| <- __top = 1
            |2. Item                               | 
            |3. Item                               |
            |4./Item///////////////////////////////| <- __cursor_y = 3, __abs_cursor_y = 4
            |5. Item                               |
            |6. Item                               |
            |7. Item                               |
            |8. Item                               | <- window_rows = 7, __bottom() = 8
            |--------------------------------------|
            |9. Item                               |
            |10. Item                              | <- __len(lines) = 10
            |                                      |
            |                                      | <- page = 1 (0 and 1)
            └--------------------------------------┘
        """
        self.__view = view
        self.__top = 0
        # current cursor position on window
        self.__cursor_y = 0
        self.__cursor_x = 0
        # Start of Nested List
        self.__root = NestedList()
        if file_path is not None:
            self.__file_path = file_path
            if os.path.exists(file_path):
                self.__root = self.load(file_path)
            else:
                self.save(file_path)
        elif root is not None:
            self.__root = root

    @property
    def __window_rows(self):
        return self.__view.num_rows

    @property
    def __window_columns(self):
        return self.__view.num_columns

    @property
    def __page(self):
        return self.__root.count() // self.__window_rows

    @property
    def __bottom(self) -> int:
        """Index of last line currently on screen"""
        return self.__top + self.__window_rows

    @property
    def __abs_cursor_y(self):
        """y axis index of cursor within lines (not screen)"""
        return self.__cursor_y + self.__top

    def __get_node(self, offset: int = 0, start: int = None):
        if start is None:
            start = self.__abs_cursor_y
        return self.__root.get_node(start + offset)

    @property
    def input_char(self) -> int:
        return self.__view.input_char

    def __correct_lateral_bounds(self):
        """
        Puts cursor back in x-axis limits if outside
        """
        node: NestedList = self.__get_node()
        left_limit: int = len(node.indent_padding)
        right_limit: int = node.width
        # put within node
        if self.__cursor_x < left_limit:
            self.__cursor_x = left_limit
        elif self.__cursor_x > right_limit:
            self.__cursor_x = right_limit
        else:  # cursor is within bounds
            field_end = node.get_selected_field_end(self.__cursor_x, LateralDirection.RIGHT)
            if field_end < self.__cursor_x:
                # if cursor in padding of field, put it at end
                self.__cursor_x = field_end

    def move(self, direction: Direction, num_spaces: int = 1):
        if isinstance(direction, LateralDirection):
            self.__cursor_x += direction * num_spaces
        else:  # VerticalDirection
            if self.__cursor_y == 0 and direction == VerticalDirection.UP \
                    or self.__cursor_y == self.__window_rows - 1 and direction == VerticalDirection.DOWN:
                # if moving past top or bottom of screen
                self.scroll(direction)
            elif direction == VerticalDirection.UP or self.__abs_cursor_y < self.__root.count() - 1:
                # not moving past bottom of buffer
                self.__cursor_y += direction * num_spaces
        self.__correct_lateral_bounds()

    def move_end(self, direction: LateralDirection):
        spaces = self.__get_node().width
        self.move(direction, spaces)

    def move_field_end(self, direction: LateralDirection):
        node = self.__get_node()
        self.__cursor_x = node.get_selected_field_end(self.__cursor_x, direction)

    def scroll(self, direction: VerticalDirection):
        """Moves the screen up or down
        Prevents the screen moving past the top or bottom of its text
        """
        # if not at absolute top or bottom of lines
        if direction == VerticalDirection.UP and self.__top > 0 \
                or direction == VerticalDirection.DOWN and self.__root.count() > self.__bottom:
            self.__top += direction

    def page(self, direction: VerticalDirection):
        """Paging the window when pressing PgUp/PgDn keys"""
        current_page = (self.__top + self.__cursor_y) // self.__window_rows
        next_page = current_page + direction
        # The last page may have fewer items than max lines,
        # so we should adjust the current cursor position as maximum item count on last page
        if next_page == self.__page:
            self.__cursor_y = min(self.__cursor_y, self.__root.count() % self.__window_rows - 1)

        # Page up
        # if current page is not a first page, page up is possible
        # __top position can not be negative, so if __top position is going to be negative, we should set it as 0
        if (direction == VerticalDirection.UP) and (current_page > 0):
            self.__top = max(0, self.__top - self.__window_rows)
            return
        # Page down
        # if current page is not a last page, page down is possible
        if (direction == VerticalDirection.DOWN) and (current_page < self.__page):
            self.__top += self.__window_rows
            return

    def display(self):
        """Display the items on window"""
        self.__view.clear()
        for abs_row_index, node in enumerate(self.__root):
            if abs_row_index < self.__top:
                # lines before the top of the screen
                continue
            row_index = abs_row_index - self.__top
            if row_index >= self.__window_rows:
                break   # stop at end of window
            # Lines within visible screen
            indent_padding = node.indent_padding
            self.__view.addstr(row_index, 0, indent_padding, Styles.EVEN)
            printed_chars = len(indent_padding)
            for field_index, text in enumerate(node.row_iter):
                """
                style changes between field
                indent precedes first field
                All but last field has trailing tab
                """
                if field_index == 0:
                    if node.collapsed:
                        style = Styles.COLLAPSED_HEADER
                    else:
                        style = Styles.HEADER
                elif field_index % 2:
                    style = Styles.EVEN
                else:
                    style = Styles.ODD
                self.__view.addstr(row_index, printed_chars, text, style)
                printed_chars += len(text)
        self.__view.move_cursor(self.__cursor_y, self.__cursor_x)
        self.__view.refresh()

    def at_root(self):
        return self.__get_node() is self.__root

    def at_line_start(self) -> bool:
        """
        :return: whether the cursor is at the start of the line (past the indent)
        """
        return self.__cursor_x == len(self.__get_node().indent_padding)

    def at_line_end(self):
        """
        :return: whether the cursor is at the start of the line (past the indent)
        """
        return self.__cursor_x == self.__get_node().width

    def at_field_end(self, direction: LateralDirection) -> bool:
        return self.__get_node().get_selected_field_end(self.__cursor_x, direction) == self.__cursor_x

    def insert(self, insertion: str):
        """
        Insert a string into the current field of the current node
        :param insertion: The string to insert
        """
        node: NestedList = self.__get_node()
        node.insert(self.__cursor_x, insertion)
        self.__cursor_x += len(insertion)

    def delete(self, x_coord_offset: int):
        """
        Delete the character at the given position
        :param x_coord_offset: the offset from the x_coord of the cursor where the character to be deleted is
        """
        node: NestedList = self.__get_node()
        node.delete_char_at(self.__cursor_x + x_coord_offset)
        self.__cursor_x += x_coord_offset

    def is_first_child(self) -> bool:
        """
        :return: whether the cursor's current node is the first child of its parent node
        Vacuously false if current is root.
        """
        current: NestedList = self.__get_node()
        if current is self.__root:
            return False
        previous: NestedList = self.__get_node(-1)
        return previous.child is current

    @property
    def current_node_has_child(self) -> bool:
        return self.__get_node().has_child

    def indent_current_node(self):
        """
        :precondition: current node cannot be first child or root
        """
        assert not self.is_first_child()
        assert not self.at_root()
        previous: NestedList = self.get_previous_sibling()
        node: NestedList = self.__get_node()
        node.indent(previous)
        self.__cursor_x += len(self.__tab)

    def unindent_current_node(self):
        parent: NestedList = self.get_parent()
        self.__get_node().unindent(parent)
        self.__cursor_x -= len(self.__tab)

    def get_previous_sibling(self) -> NestedList:
        """
        :precondition: must not be first child or root
        :return: The previous sibling of the current node
        """
        level = self.__get_node().level
        for index in reversed(range(self.__abs_cursor_y)):
            node = self.__get_node(start=index)
            if node.level == level:
                return node
            if node.level < level:
                return NullNestedList.get_instance()
        raise Exception("no previous sibling or parent found. Is this root?")

    def get_parent(self) -> NestedList:
        """
        Precondition: must not be  level 0 node
        :return: The previous sibling of the current node
        """
        parent_level = self.__get_node().level - 1
        for index in reversed(range(self.__abs_cursor_y)):
            node = self.__get_node(start=index)
            if node.level == parent_level:
                return node
        raise Exception("No parent")

    def split_field(self):
        node = self.__get_node()
        node.split_field(self.__cursor_x)
        self.__cursor_x += self.get_padding_len()

    def split_node(self):
        if self.at_line_end() or (not self.at_field_end(LateralDirection.LEFT)
                                  and not self.at_field_end(LateralDirection.RIGHT)):
            self.split_field()
        if self.at_field_end(LateralDirection.RIGHT):
            # cursor needs to be on the first field to move over for node.split()
            self.move(LateralDirection.RIGHT, self.get_padding_len())
        self.__get_node().split(self.__cursor_x)
        self.move(VerticalDirection.DOWN)
        self.move(LateralDirection.LEFT, self.__cursor_x)

    def combine_nodes(self):
        """
        removes this row and adds its fields onto the previous row
        """
        to_remove = self.__get_node()
        assert to_remove.level == 0
        # prev_row: not necessarily the previous_sibling
        prev_row: NestedList = self.__get_node(offset=-1)
        prev_sibling: NestedList = self.get_previous_sibling()
        self.move(VerticalDirection.UP)
        self.move_end(LateralDirection.RIGHT)
        to_remove.combine(prev_row, prev_sibling)
        self.move(LateralDirection.RIGHT, self.get_padding_len())

    def get_column_width(self) -> int:
        """
        :return: The width of the column at this field
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return len(node.get_padded_field(field_index))

    def get_field(self) -> str:
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return node.get_field(field_index)

    def get_neighbor_field(self, direction: LateralDirection) -> str:
        """
        :precondition: cursor cannot currently be in the first field and direction be left
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return node.get_field(field_index + direction)

    def get_padding_len(self) -> int:
        """
        :return: The length of the padding on the current field or the padding that would be on the field if it
        were not the last
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return node.get_padding_len(field_index)

    def get_neighbor_padding_len(self, direction: LateralDirection) -> int:
        """
        :precondition: cursor cannot currently be in the first field and direction be left
        :param direction:
        :return: the number of characters in the padding of the field to the right or left
        of the field inhabited by the cursor
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return node.get_padding_len(field_index + direction)

    def get_neighbor_column_width(self, direction: LateralDirection) -> int:
        """
        :precondition: cursor cannot currently be in the first field and direction be left
        :param direction:
        :return: the number of characters in the padding of the field to the right or left
        of the field inhabited by the cursor
        """
        node = self.__get_node()
        field_index = node.get_field_index(self.__cursor_x)
        return len(node.get_padded_field(field_index + direction))

    def combine_fields(self, direction: LateralDirection):
        """
        :preconditions: If direction is left, the cursor is on the left edge of the current field
            If right, it is on the right edge of the current field
        :param direction: The direction of the field that will be combined with the current field
        """
        assert self.at_field_end(direction)
        node = self.__get_node()
        # movement must be calculated before node combination, even though only used by left combine
        movement = self.get_neighbor_padding_len(direction)
        node.combine_fields(self.__cursor_x, direction)
        if direction == LateralDirection.LEFT:
            self.__cursor_x -= movement

    def signal_user_error(self):
        self.__view.signal_user_error()

    def get_level(self) -> int:
        return self.__get_node().level

    def toggle_current_node_collapsed(self):
        self.__get_node().toggle_collapsed()

    @property
    def collapsed(self) -> bool:
        return self.__get_node().collapsed

    def save(self, file_path: str = None):
        if file_path is None:
            file_path = self.__file_path
        if not file_path.endswith(self.__file_extension):
            file_path += self.__file_extension
        pickle = self.__root.serialize()
        with open(file_path, 'w') as file:
            file.write(json.dumps(pickle, indent=4))

    def load(self, file_path: str) -> NestedList:
        assert file_path.endswith(self.__file_extension)
        with open(file_path, 'r') as file:
            pickle = json.load(file)
        return NestedList.deserialize(pickle)
