#!/usr/bin/python3
import unittest
from nestingnote.nestedlist import NestedList, NullNestedList
from typing import List


class TestNestedList(unittest.TestCase):

    def test_instantiation(self):
        root = NestedList()
        self.assertTrue(isinstance(root, NestedList))
        child = root.insert_child()
        self.assertTrue(isinstance(child, NestedList))
        sibling = root.insert_sibling()
        self.assertTrue(isinstance(sibling, NestedList))

    def test_row_iter(self):
        root = NestedList(["1", "2", "3"])
        result = ''
        for field in root.row_iter:
            result += field
        target = "1    2    3"
        self.assertEqual(result, target)

    def test_delete_simple(self):
        root = NestedList(["root"])
        root.insert_sibling(["sib"])
        del root.sibling
        target = NestedList(["root"])
        self.assertEqual(root, target)
        root.insert_child(["child"])
        del root.child
        self.assertEqual(root, target)
        root.insert_sibling(["sib1"])
        root.insert_sibling(["sib2"])
        del root.sibling
        target.insert_sibling(["sib1"])
        self.assertEqual(root, target)

    def test_delete_sibling(self):
        one = NestedList(["one"])
        two = one.insert_sibling(["two"])
        three = two.insert_child(["three"])
        four = three.insert_sibling(["four"])
        five = two.insert_sibling(["five"])
        target = "one\n" \
                 + "two\n" \
                 + "    three\n" \
                 + "    four\n" \
                 + "five\n"
        actual = str(one)
        self.assertEqual(target, actual)
        del one.sibling
        target = "one\n" \
                + "    three\n" \
                + "    four\n" \
                + "five\n"
        actual = str(one)
        self.assertEqual(target, actual)

    def test_str(self):
        root = NestedList(["123", "1"])
        target = "123    1\n"
        self.assertEqual(str(root), target)
        root.insert_child(["1234"])
        target += "    1234\n"
        self.assertEqual(str(root), target)
        root.insert_sibling(["12"])
        target += "12\n"

    def test_str_complex(self):
        root = NestedList(fields=["root"])
        child = root.insert_child(texts=["child"])
        child2 = child.insert_sibling(["child2"])
        grandchild = child2.insert_child(["grandchild"])
        child3 = child2.insert_sibling(["child3"])
        child3.insert_child(["grandchild2"])

        target =     "root" \
                 + "\n    child" \
                 + "\n    child2" \
                 + "\n        grandchild" \
                 + "\n    child3" \
                 + "\n        grandchild2" \
                 + "\n"
        self.__comp_str_to_node(root, target)

    def test_columns(self):
        root = NestedList(["123", "1"])
        target = "123    1\n"
        self.__comp_str_to_node(root, target)
        root.insert_sibling(["1234"])
        target = "123     1\n"
        target += "1234\n"
        self.__comp_str_to_node(root, target)
        del root.sibling
        target = "123    1\n"
        self.__comp_str_to_node(root, target)

    def __comp_str_to_node(self, root: NestedList, target: str):
        actual = str(root)
        self.assertEqual(actual, target)

    def test_get_count(self):
        root = NestedList()
        self.assertEqual(root.count(), 1)
        sibling = root.insert_sibling()
        self.assertEqual(root.count(), 2)
        child = sibling.insert_child()
        self.assertEqual(sibling.count(), 2)
        self.assertEqual(root.count(), 3)
        grandchild = child.insert_child()
        self.assertEqual(root.count(), 4)
        grandchild2 = grandchild.insert_sibling()
        self.assertEqual(root.count(), 5)
        grandchild.insert_sibling()
        self.assertEqual(root.count(), 6)
        child.insert_sibling()
        self.assertEqual(root.count(), 7)

    def test_new_node(self):
        root = NestedList()
        child = root.insert_child()
        grandchild = child.insert_child()
        child2 = child.insert_sibling()
        self.assertIs(root.child, child)
        self.assertIs(child.sibling, child2)
        self.assertIs(root.child.child, grandchild)

    def test_get_node(self):
        root = NestedList()
        child = root.insert_child()
        grandchild = child.insert_child()
        child2 = child.insert_sibling()
        """
        root
            child
                grandchild
            child2
        """
        self.assertIs(root.get_node(0), root)
        self.assertIs(root.get_node(1), child)
        self.assertIs(root.get_node(2), grandchild)
        self.assertIs(root.get_node(3), child2)

        grandchild2 = grandchild.insert_sibling()
        child3 = child2.insert_sibling()
        greatgrandchild = grandchild.insert_child()
        """
        root
            child
                grandchild
                    greatgrandchild
                grandchild2
            child2
            child3
        """
        self.assertIs(root.get_node(0), root)
        self.assertIs(root.get_node(1), child)
        self.assertIs(root.get_node(2), grandchild)
        self.assertIs(root.get_node(3), greatgrandchild)
        self.assertIs(root.get_node(4), grandchild2)
        self.assertIs(root.get_node(5), child2)
        self.assertIs(root.get_node(6), child3)

    def __test_iter_helper(self, root: NestedList, targets: List[NestedList]):
        for index, actual in enumerate(root):
            self.assertIs(actual, targets[index])

    def test_iter(self):
        root = NestedList()
        # breakpoint()
        self.__test_iter_helper(root, [root])
        child = root.insert_child()
        self.__test_iter_helper(root, [root, child])
        child2 = child.insert_sibling()
        self.__test_iter_helper(root, [root, child, child2])
        grandchild = child2.insert_child()
        self.__test_iter_helper(root, [root, child, child2, grandchild])
        child3 = child2.insert_sibling()
        self.__test_iter_helper(root, [root, child, child2, grandchild, child3])
        greatgrandchild = grandchild.insert_child()
        self.__test_iter_helper(root, [root, child, child2, grandchild, greatgrandchild, child3])
        greatgreatgrandchild = greatgrandchild.insert_child()
        self.__test_iter_helper(root, [root, child, child2, grandchild, greatgrandchild, greatgreatgrandchild, child3])
        sibling2 = root.insert_sibling()
        sibling = root.insert_sibling()
        self.__test_iter_helper(root, [root, child, child2, grandchild, greatgrandchild, greatgreatgrandchild, child3,
                                       sibling, sibling2])

    def test_eq_simple(self):
        root = NestedList(fields=["01234"])
        self.assertEqual(root, root)
        other = NestedList(fields=["01234"])
        self.assertEqual(root, other)

    def test_eq(self):
        root = NestedList(fields=["01234"])
        child = root.insert_child(texts=["012", "0", "0"])
        child.insert_child(["012"])
        child.insert_sibling(["0", "0", "0123", ""])

        root_copy = NestedList(fields=["01234"])
        child_copy = root_copy.insert_child(texts=["012", "0", "0"])
        child_copy.insert_child(["012"])
        child_copy.insert_sibling(["0", "0", "0123", ""])

        self.assertEqual(root, root_copy)

        root_dif = NestedList(fields=["01234"])
        child_dif = root_dif.insert_child(texts=["012", "0", "0"])
        child_dif.insert_child(["012"])
        child_dif.insert_sibling(["0", "0", "0123", "9"])

        self.assertNotEqual(root, root_dif)

    def test_unindent_simple(self):
        root = NestedList(["root"])
        child = root.insert_child(["child"])
        child.unindent(root)
        target = NestedList(["root"])
        target.insert_sibling(["child"])
        self.assertEqual(root, target)

    def test_unindent(self):
        root = NestedList(["root"])
        child = root.insert_child(["child"])
        child.insert_child(["grandchild"])
        child.unindent(root)
        target = NestedList(["root"])
        sibling = target.insert_sibling(["child"])
        sibling.insert_child(["grandchild"])
        self.assertEqual(root, target)

    def test_unindent_complex(self):
        one = NestedList(fields=["one"])
        two = one.insert_child(texts=["two"])
        three = two.insert_sibling(["three"])
        three.insert_child(["four"])
        five = three.insert_sibling(["five"])
        five.insert_child(["six"])

        target =     "one" \
                 + "\n    two" \
                 + "\n    three" \
                 + "\n        four" \
                 + "\n    five" \
                 + "\n        six" \
                 + "\n"
        self.__comp_str_to_node(one, target)

        two.unindent(parent=one)
        target =     "one" \
                 + "\ntwo" \
                 + "\n    three" \
                 + "\n        four" \
                 + "\n    five" \
                 + "\n        six" \
                 + "\n"
        self.__comp_str_to_node(one, target)
        # cleanup old references
        del two
        del three
        del five

        two = one.sibling
        three = two.child
        three.unindent(parent=two)
        target =     "one" \
                 + "\ntwo" \
                 + "\nthree" \
                 + "\n    four" \
                 + "\n    five" \
                 + "\n        six" \
                 + "\n"
        self.__comp_str_to_node(one, target)

        # cleanup
        del two
        del three
        three = one.sibling.sibling
        five = three.child.sibling
        five.unindent(parent=three)
        target =     "one" \
                 + "\ntwo" \
                 + "\nthree" \
                 + "\n    four" \
                 + "\nfive" \
                 + "\n    six" \
                 + "\n"
        self.__comp_str_to_node(one, target)

    def test_serialization_simple(self):
        one = NestedList(["one", "two", "three"])
        pickle = one.serialize()
        copy = NestedList._NestedList__deserialize(pickle)
        self.assertEqual(str(one), str(copy))
        self.assertEqual(one, copy)

    def test_serialization_complex(self):
        root = NestedList(["one", "two", "three"])
        child = root.insert_child(["child1", "child2"])
        grandchild = child.insert_child(["gc1"])
        grandchild.insert_sibling(["gc2", "gc2"])
        sibling = root.insert_sibling()
        sibling.insert_sibling(["sib2", "sib2"])

        pickle = root.serialize()
        copy = NestedList._NestedList__deserialize(pickle)
        self.assertEqual(str(root), str(copy))
        self.assertEqual(root, copy)


if __name__ == '__main__':
    unittest.main()
