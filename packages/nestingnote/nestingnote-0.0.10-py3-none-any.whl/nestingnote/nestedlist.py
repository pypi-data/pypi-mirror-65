from typing import List
from nestingnote.directions import LateralDirection
from nestingnote.simpleNestedList import SimpleNestedList


class NestedList(SimpleNestedList):

    def __init__(self, fields: List[str] = None, columns=None):
        super().__init__(fields, columns)
        # are the children hidden
        self.__collapsed = False

    @staticmethod
    def _polymorphic_init(fields: List[str] = None, columns=None):
        return NestedList(fields, columns)

    def __str__(self) -> str:
        """
        For debugging and testing
        :return: string representation of Nested List starting from this node
        """
        to_return = self.indent_padding
        for text in self.row_iter:
            to_return += text
        to_return += '\n'
        to_return += str(self.child)
        to_return += str(self.sibling)
        return to_return

    def __iter__(self):
        return NestedListIterator(self)

    def __len__(self) -> int:
        raise Exception("This used to mean width")

    def get_field_index(self, x_coord: int) -> int:
        """
        :param x_coord:
        :return: index of field that the x_coordinate falls within
        """
        x_coord -= len(self.indent_padding)
        for index, field in enumerate(self.row_iter):
            ext_length = len(field)
            if x_coord < ext_length:
                return index
            x_coord -= ext_length
        return self.num_fields - 1

    def __get_field_start(self, field_index: int) -> int:
        """
        :param field_index: Which field to get the start of
        :return: The x-coord of the start of the field at the given index
        """
        assert 0 <= field_index < self.num_fields
        count = len(self.indent_padding)
        for i, field in enumerate(self.row_iter):
            if i == field_index:
                return count
            count += len(field)
        raise Exception("Unreachable")

    def __get_field_end(self, field_index: int, direction: LateralDirection) -> int:
        """
        :param field_index: Which field to get the end of
        :return: The x-coord of the left or right end of the field at the given index
        """
        start = self.__get_field_start(field_index)
        if direction == LateralDirection.LEFT:
            return start
        else:
            return start + len(self.get_field(field_index))

    def get_selected_field_end(self, x_coord: int, direction: LateralDirection) -> int:
        field_index = self.get_field_index(x_coord)
        return self.__get_field_end(field_index, direction)

    def __get_index_in_field(self, x_coord: int) -> int:
        """
        :param x_coord:
        :return: the relative position from the start of a field the coordinate is in
            FIELD: "FIELD1    "FIELD2
                    01234567890123456
            get_rel_field_index(3) == 3
            get_rel_field_index(12) == 1
        """
        x_coord -= len(self.indent_padding)
        for index, field in enumerate(self.row_iter):
            ext_length = len(field)
            if x_coord < ext_length:
                return x_coord
            x_coord -= ext_length
        # else assume at line end
        return len(self.get_field(-1))

    @property
    def null(self):
        return NullNestedList.get_instance()

    @property
    def has_child(self) -> bool:
        return self.child != self.null

    @property
    def collapsed(self) -> bool:
        return self.__collapsed

    def toggle_collapsed(self):
        self.__collapsed = not self.__collapsed

    def get_node(self, row: int):
        """
        :param row: the row the returned NestedList starts at relative to this node
        :returns: the NestedList that starts at row. None if out of bounds
        """
        if row == 0:
            return self
        row -= 1
        if not self.collapsed:
            child_count = self.child.count()
            if row < child_count:
                return self.child.get_node(row)
            row -= child_count
        sibling_count = self.sibling.count()
        if row < sibling_count:
            return self.sibling.get_node(row)
        raise IndexError("index is {} past end of NestedList".format(row))

    def count(self) -> int:
        """
        :return: the number of NestedList nodes starting from and including this
        skipping all collapsed children
        """
        nodes: int = 1
        if not self.__collapsed:
            nodes += self.child.count()
        nodes += self.sibling.count()
        return nodes

    """
    Field Editing
    """

    def insert(self, x_coord, insertion: str):
        """inserts a string into a pre-existing field"""
        field_index = self.get_field_index(x_coord)
        field: str = self.get_field(field_index)
        index = self.__get_index_in_field(x_coord)
        new_text = field[0:index] + insertion + field[index:len(field)]
        self.replace_field(field_index, new_text)

    def delete_char_at(self, x_coord: int):
        field_index = self.get_field_index(x_coord)
        field: str = self.get_field(field_index)
        index = self.__get_index_in_field(x_coord)
        new_text = field[0:index] + field[index + 1:len(field)]
        self.replace_field(field_index, new_text)

    def split_field(self, x_coord: int):
        field_index = self.get_field_index(x_coord)
        field_to_split = self.get_field(field_index)
        split_index = self.__get_index_in_field(x_coord)
        left_text = field_to_split[0:split_index]
        right_text = field_to_split[split_index:]
        self.replace_field(field_index, left_text)
        self.insert_field(field_index + 1, right_text)

    def combine_fields(self, x_coord: int, direction: LateralDirection):
        field_index = self.get_field_index(x_coord)
        current_field = self.get_field(field_index)
        other_field = self.get_field(field_index + direction)
        if direction == LateralDirection.LEFT:
            left_field = other_field
            right_field = current_field
            right_field_index = field_index
        else:
            left_field = current_field
            right_field = other_field
            right_field_index = field_index + direction
        self.replace_field(right_field_index - 1, left_field+right_field)
        self.delete_field(right_field_index)

    """
    Edit Node
    """

    def indent(self, prev_sibling: SimpleNestedList):
        """
        makes this node's sibling his child, and its sibling's sibling, its sibling
        """
        assert prev_sibling is not self.null
        new_child = prev_sibling.append_child(self.fields)
        new_child._insert_sibling_deep(self.child)
        del prev_sibling.sibling.child
        del prev_sibling.sibling

    def unindent(self, parent: SimpleNestedList):
        """
        :param parent: The parent of this node or one of its older siblings
        """
        assert parent is not self.null
        new_self = parent.insert_sibling(self.fields)
        new_self._insert_child_deep(self.child)
        # append sibling family onto child
        new_self._append_child_deep(self.sibling)

        # delete old reference
        if parent.child is self:
            del parent.child
        else:
            indented_node = parent.child
            next_child = indented_node.sibling
            while next_child is not self:
                indented_node = next_child
                next_child = indented_node.sibling
            # delete reference to self and all descendants
            indented_node.delete_sibling_deep()

    def split(self, x_coord: int):
        """
        Create a new node as a sibling with all fields right of the x_coord, inclusive
        These fields are removed from this node
        Does not split the field itself, only the row
        :param x_coord: The row is split at the field containing the x_coord
        """
        field_index = self.get_field_index(x_coord)
        split_fields: List[str] = []
        for index in range(self.num_fields - field_index):
            field = self.get_field(field_index)
            split_fields.append(field)
            self.delete_field(field_index)
        new_sibling = self.insert_sibling(split_fields)
        new_sibling._insert_child_deep(self.child)
        del self.child

    def combine(self, previous_node: SimpleNestedList, prev_sibling: SimpleNestedList):
        """
        Removes this row from its tree and adds its fields to previous_node
        :param previous_node: The row to add self's fields to
        """
        for field in self.fields:
            previous_node.append_field(field)
        del prev_sibling.sibling

    # Serialization

    def serialize(self) -> dict:
        return {
            "fields": self.fields,
            "child": self.child.serialize(),
            "sibling": self.sibling.serialize()
        }

    @classmethod
    def deserialize(cls, pickle: dict):
        node = NestedList(pickle['fields'])
        node._deserialize_helper(pickle)
        return node

    def _deserialize_helper(self, pickle: dict):
        if pickle['child'] is not None:
            child = self.insert_child(pickle['child']['fields'])
            child._deserialize_helper(pickle['child'])
        if pickle['sibling'] is not None:
            sibling = self.insert_sibling(pickle['sibling']['fields'])
            sibling._deserialize_helper(pickle['sibling'])


class NestedListIterator:
    def __init__(self, root: NestedList):
        class FakeNestedList(NestedList):
            def __init__(self, child):
                self.__child = child

            @property
            def child(self):
                return self.__child

            @property
            def sibling(self):
                return NullNestedList.get_instance()

            @property
            def collapsed(self) -> bool:
                return False

        # fake node parenting root for cleaner loop in iterator
        first = FakeNestedList(root)
        self.previous: List[NestedList] = [first]

    def __next__(self):
        next_node = self.previous[-1].child
        if not isinstance(next_node, NullNestedList) and not self.previous[-1].collapsed:
            self.previous.append(next_node)
            return next_node
        while len(self.previous) > 0:
            next_node = self.previous.pop().sibling
            if not isinstance(next_node, NullNestedList):
                self.previous.append(next_node)
                return next_node
        raise StopIteration


class NullNestedList(NestedList):
    """
    Marks the ends of Nested List branches
    Vacuously implements all NestedList methods
    """
    __instance = None

    @staticmethod
    def get_instance():
        if NullNestedList.__instance is None:
            NullNestedList.__instance = NullNestedList()
        return NullNestedList.__instance

    def __init__(self):
        """private constructor"""
        if NullNestedList.__instance is not None:
            raise Exception("This class is a singleton")
        else:
            NullNestedList.__instance = self

    def __eq__(self, other) -> bool:
        return other is self

    def __len__(self) -> int:
        return 0

    def __str__(self) -> str:
        return ''

    @property
    def _columns(self):
        """
        For creating a new array of columns when the new node has no sibling
        """
        return []

    @property
    def fields(self) -> List[str]:
        raise Exception("Not allowed for NullRow")

    @property
    def child(self):
        return self

    @property
    def sibling(self):
        return self

    @property
    def level(self):
        raise Exception("Not allowed for NullRow")

    @property
    def last_sibling(self):
        raise Exception("Should not be called on NullNestedList")

    def _attach_to_parent(self, parent):
        return self

    def _attach_to_prev_sibling(self, prev_sibling):
        return self

    def _insert_child_deep(self, parent):
        pass

    def _append_child_deep(self, new_child):
        pass

    def _insert_sibling_deep(self, prev_sibling):
        pass

    def __del__(self):
        pass

    def get_last_child(self, stop_before=None):
        raise Exception("Should not be called on a NullNestedList")

    def get_node(self, row: int):
        raise Exception("Should not be called on a NullNestedList")

    def count(self) -> int:
        return 0

    def insert_child(self, texts: List[str] = None):
        raise Exception("Should not be called on a NullNestedList")

    def insert_sibling(self, fields: List[str] = None):
        raise Exception("Should not be called on a NullNestedList")

    @child.deleter
    def child(self):
        raise Exception("Should not be called on a NullNestedList")

    @sibling.deleter
    def sibling(self):
        raise Exception("Should not be called on a NullNestedList")

    def insert(self, x_coord, insertion: str):
        raise Exception("Should not be called on a NullNestedList")

    def insert_field(self, text: str, insert_index: int):
        raise Exception("Should not be called on a NullNestedList")

    def split(self, x_coord: int):
        raise Exception("Should not be called on a NullNestedList")

    def split_field(self, x_coord: int):
        raise Exception("Should not be called on a NullNestedList")

    def _append_child(self, new_child):
        raise Exception("Should not be called on a NullNestedList")

    def serialize(self) -> dict:
        return None

    def _deserialize_helper(self, pickle: dict):
        pass
