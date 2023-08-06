from typing import List
from nestingnote.row import Row
from nestingnote.column import Column


class SimpleNestedList(object):
    """
    This is an abstract class because of its self.null abstract method
    Encapsulates the column and level data
    """

    __indent_len = 4

    def __init__(self, fields: List[str] = None, columns: List[Column] = None):
        """
        :param fields:
        :param columns: Should only be used privately by SimpleNestedList.
            Unfortunately, python does not support private constructors.
        """
        if fields is None:
            fields = []
        if columns is None:
            columns = []
        self.__columns = columns
        self.__row = Row(columns, fields)
        # links to neighboring nested list nodes
        self.__child = self.null
        self.__sibling = self.null
        # indentation level
        self.__level = 0

    @staticmethod
    def _polymorphic_init(fields: List[str] = None, columns: List[Column] = None):
        """
        For polymorphic instantiation used by new_nested_list
        Should be overriden to return an instance of whatever subclass of SimpleNestedList calls this.
        :return: subclass of SimpleNestedList
        """
        return SimpleNestedList(fields, columns)

    @classmethod
    def _new_nested_list(cls, level: int, columns: List[Column], fields: List[str] = None,
                         next_sibling=None, first_child=None):
        """
        Virtual private constructor
        Depends upon the overriding of the polymorphic_init method
        :return: new NestedList
        """
        if fields is None:
            fields = []
        node = cls._polymorphic_init(fields, columns)
        node.__level = level
        if next_sibling is not None:
            node.__sibling = next_sibling
        if first_child is not None:
            node.__child = first_child
        return node

    def __del__(self):
        self.__row = None

    # Abstract properties

    @property
    def null(self):
        raise Exception("Abstract property")
        # return _NullSimpleNestedList.getInstance()

    # Protected methods

    def _attach_to_parent(self, parent):
        """
        Reverse of insert_child, used to allow NullNestedList to polymophically handle child insertion
        differently.
        Inserts the fields of self into the context of parent
        Use instead of insert_child when you want the insertion to only happen if self is not null
        :param parent: node to insert self under
        :return: The new instance of self that is now attached to prev_sibling
        """
        return parent.insert_child(self.fields)

    def _attach_to_prev_sibling(self, prev_sibling):
        """
        Reverse of insert_sibling, used to allow NullNestedList to polymophically handle sibling insertion
        differently.
        Inserts the fields of self into the context of prev_sibling
        Use instead of insert_sibling when you want the insertion to only happen if self is not null
        :param prev_sibling: node to insert self under
        :return: The new instance of self that is now attached to prev_sibling
        """
        return prev_sibling.insert_sibling(self.fields)

    def _insert_sibling_deep(self, sibling):
        """
        Inserts a nestedList node and all its descendants as a sibling under self
        :param sibling:
        """
        new_sibling = sibling._attach_to_prev_sibling(prev_sibling=self)
        new_sibling._insert_child_deep(sibling.child)
        new_sibling._insert_sibling_deep(sibling.sibling)

    def _append_child_deep(self, new_child):
        """
        Inserts a nestedList node and all its descendants as a child under self's last child
        :param new_child: node whose fields and descendants are to be inserted as a new nestedlist under
        self's last child
        """
        if self.child is self.null:
            self._insert_child_deep(new_child)
        else:
            self.last_child._insert_sibling_deep(new_child)

    def _insert_child_deep(self, child):
        """
        Inserts a nestedList node and all its descendants as a child under self
        :param child: node whose fields and descendants are to be inserted as a new nestedlist under self
        """
        new_child = child._attach_to_parent(parent=self)
        new_child._insert_child_deep(child.child)
        new_child._insert_sibling_deep(child.sibling)

    # Properties

    @property
    def _columns(self):
        """
        For polymorphism with _NullRow
        """
        # TODO make an inner class node and use decorator getters and setters
        return self.__columns


    @property
    def last_sibling(self):
        """
        :return: Last sibling on this level of a nested list
        """
        if self.sibling is self.null:
            return self
        return self.sibling.last_sibling

    @property
    def last_child(self):
        return self.child.last_sibling

    @property
    def level(self):
        return self.__level

    def _set_level(self, new_level: int):
        self.__level = new_level
        self.__child._set_level(new_level)
        self.__sibling._set_level(new_level)

    @property
    def sibling(self):
        return self.__sibling

    @sibling.deleter
    def sibling(self):
        """
        Deletes the sibling row only, not its children or siblings
        The sibling is replaced by this.sibling.sibling and its children are given to this
        """
        nephew = self.sibling.child
        if nephew is not self.null:
            self._append_child_deep(nephew)
        self.__sibling = self.sibling.sibling

    def delete_sibling_deep(self):
        """
        Deletes the sibling row and all its siblings and children
        """
        self.__sibling = self.null

    def insert_sibling(self, texts: List[str] = None):
        if texts is None:
            texts = []
        self.__sibling = self._new_nested_list(columns=self._columns, fields=texts,
                                               level=self.__level, next_sibling=self.__sibling)
        return self.__sibling

    @property
    def child(self):
        return self.__child

    @child.deleter
    def child(self):
        """
        Deletes the child row and all children, siblings, and descendants recursively
        """
        self.__child = self.null

    def append_child(self, texts: List[str] = None):
        """
        Adds new child as the last child under this
        :param texts: fields to appear in the new child
        :return: The new child appended
        """
        if self.__child is self.null:
            return self.insert_child(texts)
        # else this has at least one child
        last_child = self.__child.last_sibling
        return last_child.insert_sibling(texts)

    def insert_child(self, texts: List[str] = None):
        if texts is None:
            texts = []
        child_cols = self.__child._columns
        self.__child = self._new_nested_list(columns=child_cols, fields=texts,
                                             level=self.__level + 1, next_sibling=self.__child)
        return self.__child

    @property
    def indent_padding(self) -> str:
        return (' ' * self.__indent_len) * self.level

    """
    Row operations
    """

    @property
    def fields(self) -> List[str]:
        return self.__row.fields

    @property
    def num_fields(self) -> int:
        return len(self.__row)

    @property
    def row_iter(self):
        return iter(self.__row)

    @property
    def unpadded_row_iter(self):
        return self.__row.unpadded_iter

    @property
    def width(self) -> int:
        """
        :return: num characters in string representation of fields including indentation and separation
        """
        return self.__row.width() + len(self.indent_padding)

    def insert_field(self, index: int, text: str):
        self.__row.insert(index, text)

    def append_field(self, text: str):
        self.__row.append(text)

    def delete_field(self, index):
        self.__row.remove(index)

    def replace_field(self, index: int, replacement: str):
        self.__row.replace(index, replacement)

    def get_field(self, index: int) -> str:
        return self.__row.field(index)

    def get_padded_field(self, index: int) -> str:
        return self.__row.padded_field(index)

    def get_padding_len(self, index: int) -> int:
        return self.__row.padding_len(index)

    def __eq__(self, other) -> bool:
        if not isinstance(other, SimpleNestedList):
            return False
        return self.__row == other.__row and \
            self.child == other.child and \
            self.sibling == other.sibling

