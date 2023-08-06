import unittest
from nestingnote.model import Model
from nestingnote.testView import TestView
from nestingnote.nestedlist import NestedList
from nestingnote.directions import LateralDirection, VerticalDirection


class MyTestCase(unittest.TestCase):

    # Getters

    def test_get_node(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = one.insert_sibling(["three"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model._Model__get_node(), one)
        model._Model__cursor_y = 1
        self.assertEqual(model._Model__get_node(), two)
        model._Model__cursor_y = 2
        self.assertEqual(model._Model__get_node(), three)
        four = two.insert_child(["four"])
        """
        one
            two
                four
        three
        """
        model._Model__cursor_y = 2
        self.assertEqual(model._Model__get_node(), four)
        five = one.insert_sibling(["five"])
        """
        one
            two
                four
        five
        three
        """
        model._Model__cursor_y = 3
        self.assertEqual(model._Model__get_node(), five)

    def test_get_level(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = one.insert_sibling(["three"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        self.assertEqual(model.get_level(), 0)
        model._Model__cursor_y = 1
        self.assertEqual(model.get_level(), 1)
        model._Model__cursor_y = 2
        self.assertEqual(model.get_level(), 0)

    def test_get_previous_sibling(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = two.insert_sibling(["three"])
        four = one.insert_sibling(["four"])
        """
        one
            two
            three
        four
        """
        model = Model(TestView([]), one)
        model._Model__cursor_y = 3
        self.assertIs(one, model.get_previous_sibling())
        model._Model__cursor_y = 2
        self.assertIs(two, model.get_previous_sibling())

    def test_get_parent(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = two.insert_sibling(["three"])
        four = one.insert_sibling(["four"])
        five = four.insert_child(["five"])
        """
        one
            two
            three
        four
            five
        """
        model = Model(TestView([]), one)
        model._Model__cursor_y = 2
        self.assertIs(one, model.get_parent())
        model._Model__cursor_y = 4
        self.assertIs(four, model.get_parent())

    def test_get_column_width(self):
        one = NestedList(["one", "two.", "three"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_column_width(), 7)
        model._Model__cursor_x = 2
        self.assertEqual(model.get_column_width(), 7)
        model._Model__cursor_x = 6
        self.assertEqual(model.get_column_width(), 7)
        model._Model__cursor_x = 7
        self.assertEqual(model.get_column_width(), 8)
        model._Model__cursor_x = 11
        self.assertEqual(model.get_column_width(), 8)
        model._Model__cursor_x = 15
        self.assertEqual(model.get_column_width(), 9)
        model._Model__cursor_x = 20
        self.assertEqual(model.get_column_width(), 9)

    def test_get_neighbor_column_width(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        one = NestedList(["one", "two.", "three"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_neighbor_column_width(right), 8)
        model._Model__cursor_x = 2
        self.assertEqual(model.get_neighbor_column_width(right), 8)
        model._Model__cursor_x = 6
        self.assertEqual(model.get_neighbor_column_width(right), 8)
        model._Model__cursor_x = 7
        self.assertEqual(model.get_neighbor_column_width(right), 9)
        self.assertEqual(model.get_neighbor_column_width(left), 7)
        model._Model__cursor_x = 11
        self.assertEqual(model.get_neighbor_column_width(right), 9)
        self.assertEqual(model.get_neighbor_column_width(left), 7)
        model._Model__cursor_x = 15
        self.assertEqual(model.get_neighbor_column_width(left), 8)
        model._Model__cursor_x = 20
        self.assertEqual(model.get_neighbor_column_width(left), 8)

    def test_get_neighbor_field(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        fields = ["one", "two.", "three"]
        one = NestedList(fields)
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_neighbor_field(right), fields[1])
        model._Model__cursor_x = 2
        self.assertEqual(model.get_neighbor_field(right), fields[1])
        model._Model__cursor_x = 6
        self.assertEqual(model.get_neighbor_field(right), fields[1])
        model._Model__cursor_x = 7
        self.assertEqual(model.get_neighbor_field(right), fields[2])
        self.assertEqual(model.get_neighbor_field(left), fields[0])
        model._Model__cursor_x = 11
        self.assertEqual(model.get_neighbor_field(right), fields[2])
        self.assertEqual(model.get_neighbor_field(left), fields[0])
        model._Model__cursor_x = 15
        self.assertEqual(model.get_neighbor_field(left), fields[1])
        model._Model__cursor_x = 20
        self.assertEqual(model.get_neighbor_field(left), fields[1])

    def test_get_padding_len(self):
        one = NestedList(["one", "two.", "three"])
        one.insert_sibling(["one", "two.5", "three56"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_padding_len(), 4)
        model._Model__cursor_x = 2
        self.assertEqual(model.get_padding_len(), 4)
        model._Model__cursor_x = 6
        self.assertEqual(model.get_padding_len(), 4)
        model._Model__cursor_x = 7
        self.assertEqual(model.get_padding_len(), 5)
        model._Model__cursor_x = 11
        self.assertEqual(model.get_padding_len(), 5)
        model._Model__cursor_x = 16
        self.assertEqual(model.get_padding_len(), 6)
        model._Model__cursor_x = 21
        self.assertEqual(model.get_padding_len(), 6)

    def test_get_neighbor_padding_len(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        one = NestedList(["one", "two.", "three"])
        one.insert_sibling(["one", "two.5", "three56"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertEqual(model.get_neighbor_padding_len(right), 5)
        model._Model__cursor_x = 2
        self.assertEqual(model.get_neighbor_padding_len(right), 5)
        model._Model__cursor_x = 6
        self.assertEqual(model.get_neighbor_padding_len(right), 5)
        model._Model__cursor_x = 7
        self.assertEqual(model.get_neighbor_padding_len(right), 6)
        self.assertEqual(model.get_neighbor_padding_len(left), 4)
        model._Model__cursor_x = 11
        self.assertEqual(model.get_neighbor_padding_len(right), 6)
        self.assertEqual(model.get_neighbor_padding_len(left), 4)
        model._Model__cursor_x = 16
        self.assertEqual(model.get_neighbor_padding_len(left), 5)
        model._Model__cursor_x = 21
        self.assertEqual(model.get_neighbor_padding_len(left), 5)

    # Location Getters

    def test_is_first_child(self):
        root = NestedList(["root"])
        child = root.insert_child(["child"])
        child2 = child.insert_sibling(["child2"])
        grandchild = child2.insert_child(["grandchild"])
        grandchild2 = grandchild.insert_sibling(["grandchild2"])
        child3 = child2.insert_sibling(["child3"])
        """
        root
            child
            child2
                grandchild
                grandchild2
            child3
        """
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        self.assertFalse(model.is_first_child())
        model._Model__cursor_y = 1
        self.assertTrue(model.is_first_child())
        model._Model__cursor_y = 2
        self.assertFalse(model.is_first_child())
        model._Model__cursor_y = 3
        self.assertTrue(model.is_first_child())
        model._Model__cursor_y = 4
        self.assertFalse(model.is_first_child())
        model._Model__cursor_y = 5
        self.assertFalse(model.is_first_child())

    def test_at_root(self):
        root = NestedList(["root"])
        child = root.insert_child(["child"])
        child2 = child.insert_sibling(["child2"])
        grandchild = child2.insert_child(["grandchild"])
        grandchild2 = grandchild.insert_sibling(["grandchild2"])
        child3 = child2.insert_sibling(["child3"])
        """
        root
            child
            child2
                grandchild
                grandchild2
            child3
        """
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        self.assertTrue(model.at_root())
        model._Model__cursor_y = 1
        self.assertFalse(model.at_root())
        model._Model__cursor_y = 2
        self.assertFalse(model.at_root())
        model._Model__cursor_y = 3
        self.assertFalse(model.at_root())
        model._Model__cursor_y = 4
        self.assertFalse(model.at_root())
        model._Model__cursor_y = 5
        self.assertFalse(model.at_root())

    def test_at_line_start(self):
        root = NestedList(["root"])
        child = root.insert_child(["child"])
        child2 = child.insert_sibling(["child2"])
        grandchild = child2.insert_child(["grandchild"])
        grandchild2 = grandchild.insert_sibling(["grandchild2"])
        child3 = child2.insert_sibling(["child3"])
        """
        root
            child
            child2
                grandchild
                grandchild2
            child3
        """
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        self.assertTrue(model.at_line_start())
        model._Model__cursor_x = 1
        self.assertFalse(model.at_line_start())

        model._Model__cursor_y = 1
        model._Model__cursor_x = 4
        self.assertTrue(model.at_line_start())
        model._Model__cursor_x = 5
        self.assertFalse(model.at_line_start())

        model._Model__cursor_y = 2
        model._Model__cursor_x = 4
        self.assertTrue(model.at_line_start())
        model._Model__cursor_x = 5
        self.assertFalse(model.at_line_start())

        model._Model__cursor_y = 3
        model._Model__cursor_x = 8
        self.assertTrue(model.at_line_start())
        model._Model__cursor_x = 9
        self.assertFalse(model.at_line_start())

        model._Model__cursor_y = 4
        model._Model__cursor_x = 8
        self.assertTrue(model.at_line_start())
        model._Model__cursor_x = 9
        self.assertFalse(model.at_line_start())

        model._Model__cursor_y = 5
        model._Model__cursor_x = 4
        self.assertTrue(model.at_line_start())
        model._Model__cursor_x = 5
        self.assertFalse(model.at_line_start())

    def test_at_line_end(self):
        root = NestedList(["root"])
        child = root.insert_child(["child", "child"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 4
        self.assertTrue(model.at_line_end())
        model._Model__cursor_x = 3
        self.assertFalse(model.at_line_end())

        model._Model__cursor_y = 1
        model._Model__cursor_x = 18
        self.assertTrue(model.at_line_end())
        model._Model__cursor_x = 17
        self.assertFalse(model.at_line_end())

    def test_at_field_end(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        root = NestedList(["root"])
        child = root.insert_child(["child", "child"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 0
        # root
        self.assertFalse(model.at_field_end(right))
        self.assertTrue(model.at_field_end(left))
        model._Model__cursor_x = 4
        self.assertTrue(model.at_field_end(right))
        self.assertFalse(model.at_field_end(left))
        model._Model__cursor_x = 3
        self.assertFalse(model.at_field_end(right))
        self.assertFalse(model.at_field_end(left))
        # child
        model._Model__cursor_y = 1
        model._Model__cursor_x = 4
        self.assertTrue(model.at_field_end(left))
        self.assertFalse(model.at_field_end(right))
        model._Model__cursor_y = 1
        model._Model__cursor_x = 9
        self.assertTrue(model.at_field_end(right))
        self.assertFalse(model.at_field_end(left))
        model._Model__cursor_y = 1
        model._Model__cursor_x = 13
        self.assertTrue(model.at_field_end(left))
        self.assertFalse(model.at_field_end(right))
        model._Model__cursor_y = 1
        model._Model__cursor_x = 18
        self.assertTrue(model.at_field_end(right))
        self.assertFalse(model.at_field_end(left))
        model._Model__cursor_x = 17
        self.assertFalse(model.at_field_end(right))

    # Actions

    def test_move_lateral(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        root = NestedList(["root", "node"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 3
        model.move(right)
        self.assertEqual(model._Model__cursor_x, 4)
        model.move(right)
        # will be brought back to end of field
        self.assertEqual(model._Model__cursor_x, 4)
        model.move(right, 4)
        self.assertEqual(model._Model__cursor_x, 8)
        model.move(right)
        self.assertEqual(model._Model__cursor_x, 9)
        model.move(left)
        self.assertEqual(model._Model__cursor_x, 8)
        model.move(left)
        self.assertEqual(model._Model__cursor_x, 4)

    def test_move_vertical(self):
        up = VerticalDirection.UP
        down = VerticalDirection.DOWN
        one = NestedList(["one", "one"])
        two = one.insert_sibling(["two"])
        three = two.insert_sibling(["3"])
        four = three.insert_sibling([""])
        five = four.insert_sibling()
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 8
        model.move(down)
        self.assertEqual(model._Model__cursor_x, 3)
        self.assertEqual(model._Model__cursor_y, 1)
        model.move(down)
        self.assertEqual(model._Model__cursor_x, 1)
        self.assertEqual(model._Model__cursor_y, 2)
        model.move(down)
        self.assertEqual(model._Model__cursor_x, 0)
        self.assertEqual(model._Model__cursor_y, 3)
        model.move(down)
        self.assertEqual(model._Model__cursor_x, 0)
        self.assertEqual(model._Model__cursor_y, 4)

    def test_move_end(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        root = NestedList(["root", "node"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 2
        model.move_end(right)
        self.assertEqual(model._Model__cursor_x, 12)
        model.move_end(left)
        self.assertEqual(model._Model__cursor_x, 0)

    def test_move_field_end(self):
        right = LateralDirection.RIGHT
        left = LateralDirection.LEFT
        root = NestedList(["root", "node"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 2
        model.move_field_end(right)
        self.assertEqual(model._Model__cursor_x, 4)
        model.move_field_end(left)
        self.assertEqual(model._Model__cursor_x, 0)

    def test_delete(self):
        root = NestedList(["root", "node"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 3
        model.delete(0)
        self.assertEqual(model.get_field(), "roo")
        model.delete(-1)
        self.assertEqual(model.get_field(), "ro")

    def test_insert(self):
        root = NestedList(["root", "node"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 4
        model.insert('s')
        self.assertEqual(model.get_field(), "roots")

    def test_split_field(self):
        root = NestedList(["root", "node"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 3
        model.split_field()
        fields = str(model._Model__root)
        target = 'roo    t    node\n'
        self.assertEqual(fields, target)

    def test_combine_field_right(self):
        root = NestedList(["root", "node"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 4
        model.combine_fields(LateralDirection.RIGHT)
        fields = str(model._Model__root)
        target = 'rootnode\n'
        self.assertEqual(fields, target)
        self.assertEqual(model._Model__cursor_x, 4)

    def test_combine_field_left(self):
        root = NestedList(["root", "node"])
        model = Model(TestView([]), root)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 8
        model.combine_fields(LateralDirection.LEFT)
        fields = str(model._Model__root)
        target = 'rootnode\n'
        self.assertEqual(fields, target)
        self.assertEqual(model._Model__cursor_x, 4)

    def test_indent_current_node(self):
        one = NestedList(["one"])
        two = one.insert_sibling(["two"])
        three = two.insert_sibling(["three"])
        three.insert_sibling(["four"])
        model = Model(TestView([]), one)
        model._Model__cursor_y = 0
        self.assertRaises(Exception, lambda: model.indent_current_node())
        model._Model__cursor_y = 1
        model.indent_current_node()
        target = 'one\n' \
                + '    two\n' \
                + 'three\n' \
                + 'four\n'
        actual = str(one)
        self.assertEqual(target, actual)
        model._Model__cursor_y = 2
        model.indent_current_node()
        target = 'one\n' \
                 + '    two\n' \
                 + '    three\n' \
                 + 'four\n'
        actual = str(one)
        self.assertEqual(target, actual)
        model._Model__cursor_y = 3
        model.indent_current_node()
        target = 'one\n' \
                 + '    two\n' \
                 + '    three\n' \
                 + '    four\n'
        actual = str(one)
        self.assertEqual(target, actual)
        model._Model__cursor_y = 2
        model.indent_current_node()
        target = 'one\n' \
                 + '    two\n' \
                 + '        three\n' \
                 + '    four\n'
        actual = str(one)
        self.assertEqual(target, actual)
        model._Model__cursor_y = 3
        model.indent_current_node()
        target = 'one\n' \
                 + '    two\n' \
                 + '        three\n' \
                 + '        four\n'
        actual = str(one)
        self.assertEqual(target, actual)
        model._Model__cursor_y = 3
        model.indent_current_node()
        target = 'one\n' \
                 + '    two\n' \
                 + '        three\n' \
                 + '            four\n'
        actual = str(one)
        self.assertEqual(target, actual)

    def test_unindent_current_node_simple(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        model = Model(TestView([]), one)
        target = 'one\n' \
                 + '    two\n'
        actual = str(one)
        self.assertEqual(target, actual)
        self.assertRaises(Exception, lambda: model.indent_current_node())
        model._Model__cursor_y = 1
        model.unindent_current_node()
        target =   'one\n' \
                 + 'two\n'
        actual = str(one)
        self.assertEqual(target, actual)

    def test_unindent_current_node_complex(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = two.insert_sibling(["three"])
        four = three.insert_child(["four"])
        four.insert_sibling(["five"])
        six = three.insert_sibling(["six"])
        six.insert_sibling(["seven"])
        one.insert_sibling(["eight"])
        model = Model(TestView([]), one)
        target =   'one\n' \
                 + '    two\n' \
                 + '    three\n' \
                 + '        four\n' \
                 + '        five\n' \
                 + '    six\n' \
                 + '    seven\n' \
                 + 'eight\n'
        actual = str(one)
        self.assertEqual(target, actual)
        self.assertRaises(Exception, lambda: model.indent_current_node())
        model._Model__cursor_y = 2
        model.unindent_current_node()
        target =   'one\n' \
                 + '    two\n' \
                 + 'three\n' \
                 + '    four\n' \
                 + '    five\n' \
                 + '    six\n' \
                 + '    seven\n' \
                 + 'eight\n'
        actual = str(one)
        self.assertEqual(target, actual)

    def test_combine_nodes_simple(self):
        one = NestedList(["one"])
        two = one.insert_sibling(["two"])
        model = Model(TestView([]), one)
        target =   'one\n' \
                 + 'two\n'
        actual = str(one)
        self.assertEqual(target, actual)
        model._Model__cursor_y = 1
        model.combine_nodes()
        target = 'one    two\n'
        actual = str(one)
        self.assertEqual(target, actual)

    def test_combine_nodes_complex(self):
        one = NestedList(["one"])
        two = one.insert_child(["two"])
        three = two.insert_child(["three"])
        three.insert_child(["four", "four", "four"])
        five = one.insert_sibling(["five", "five", "five"])
        five.insert_child(["six"])
        model = Model(TestView([]), one)
        target = 'one\n' \
                 + '    two\n' \
                 + '        three\n' \
                 + '            four    four    four\n' \
                 + 'five    five    five\n' \
                 + '    six\n'
        actual = str(one)
        self.assertEqual(target, actual)
        model._Model__cursor_y = 4
        model.combine_nodes()
        target = 'one\n' \
                 + '    two\n' \
                 + '        three\n' \
                 + '            four    four    four    five    five    five\n' \
                 + '    six\n'
        actual = str(one)
        self.assertEqual(target, actual)

    def test_split_node_simple(self):
        root = NestedList(["one", "two", "three"])
        model = Model(TestView([]), root)
        target = "one    two    three\n"
        actual = str(root)
        self.assertEqual(target, actual)
        model._Model__cursor_y = 0
        model._Model__cursor_x = 8
        model.split_node()
        target =  "one    t\n" \
                + "wo     three\n"
        actual = str(root)
        self.assertEqual(target, actual)

    def test_split_node_complex(self):
        root = NestedList(["root"])
        one = root.insert_child(["one", "two", "three"])
        one.insert_child(["two"])
        one.insert_sibling(["three"])
        model = Model(TestView([]), root)
        target = "root\n" \
                + "    one      two    three\n" \
                + "        two\n" \
                + "    three\n"
        actual = str(root)
        self.assertEqual(actual, target)
        model._Model__cursor_y = 1
        model._Model__cursor_x = 14
        model.split_node()
        target = "root\n" \
                + "    one      t\n" \
                + "    wo       three\n" \
                + "        two\n" \
                + "    three\n"
        actual = str(root)
        self.assertEqual(actual, target)

    def test_split_node_end(self):
        root = NestedList(["root"])
        one = root.insert_child(["one", "two", "three"])
        one.insert_child(["two"])
        one.insert_sibling(["three"])
        model = Model(TestView([]), root)
        target = "root\n" \
                 + "    one      two    three\n" \
                 + "        two\n" \
                 + "    three\n"
        actual = str(root)
        self.assertEqual(actual, target)
        model._Model__cursor_y = 1
        model._Model__cursor_x = 25
        model.split_node()
        target = "root\n" \
                 + "    one      two    three\n" \
                 + "    \n" \
                 + "        two\n" \
                 + "    three\n"
        actual = str(root)
        self.assertEqual(actual, target)

    def test_split_node_start(self):
        root = NestedList(["root"])
        one = root.insert_child(["one", "two", "three"])
        one.insert_child(["two"])
        one.insert_sibling(["three"])
        model = Model(TestView([]), root)
        target = "root\n" \
                 + "    one      two    three\n" \
                 + "        two\n" \
                 + "    three\n"
        actual = str(root)
        self.assertEqual(actual, target)
        model._Model__cursor_y = 1
        model._Model__cursor_x = 4
        model.split_node()
        target = "root\n" \
                 + "    \n" \
                 + "    one      two    three\n" \
                 + "        two\n" \
                 + "    three\n"
        actual = str(root)
        self.assertEqual(actual, target)

    def test_save_and_load(self):
        root = NestedList(["one", "two", "three"])
        child = root.insert_child(["child1", "child2"])
        grandchild = child.insert_child(["gc1"])
        grandchild.insert_sibling(["gc2", "gc2"])
        sibling = root.insert_sibling()
        sibling.insert_sibling(["sib2", "sib2"])
        file_path = '/tmp/nestedlist.nnn'
        model = Model(TestView([]), root=root)
        model.save(file_path)
        del model
        model = Model(TestView([]), file_path)
        copy = model._Model__root
        self.assertEqual(str(root), str(copy))
        self.assertEqual(root, copy)


if __name__ == '__main__':
    unittest.main()
