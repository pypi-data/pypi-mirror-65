#!/usr/bin/python3
import unittest
from nestingnote.row import Row
from typing import List


class TestRow(unittest.TestCase):

    def test_eq(self):
        row = Row(columns=[], fields=["one", "two", "three"])
        self.assertEqual(row, row)
        row2 = Row(columns=[], fields=["one", "two", "three"])
        self.assertEqual(row, row2)
        columns = []
        row3 = Row(columns, fields=["one", "two", "three"])
        # causes row3 to have an extra column, but shouldn't affect equality
        other = Row(columns, fields=["one", "two", "three", ""])
        self.assertEqual(row, row3)
        row_diff = Row(columns=[], fields=["one", "two", "threeE"])
        self.assertNotEqual(row, row_diff)
        row_diff2 = Row(columns=[], fields=["one", "two"])
        self.assertNotEqual(row, row_diff2)
        diff_columns = []
        row_diff3 = Row(diff_columns, ["one", "two", "three"])
        # creates a different column width in the first column of row_diff3
        row_other = Row(diff_columns, ["1234"])
        self.assertNotEqual(row, row_diff3)

    def test_columns(self):
        """
        Tests consistency of column lengths when rows are created or deleted with the same list of columns
        """
        columns = []
        one = Row(columns, fields=["123", "123", "12345"])
        self.__test_columns_helper([one], [7, 7, 9])
        two = Row(columns, fields=["1", "1", "1"])
        self.__test_columns_helper([one, two], [7, 7, 9])
        three = Row(columns, fields=["1234", "1234567", "123"])
        self.__test_columns_helper([one, two, three], [8, 11, 9])
        del one
        self.__test_columns_helper([two, three], [8, 11, 7])
        del three
        self.__test_columns_helper([two], [5, 5, 5])
        four = Row(columns)
        self.__test_columns_helper([two], [5, 5, 5])
        four.append("56")
        self.__test_columns_helper([two], [6, 5, 5])
        four.insert(0, "567")
        self.__test_columns_helper([two], [7, 6, 5])
        four.insert(2, "5678")
        self.__test_columns_helper([two], [7, 6, 8])
        four.remove(0)
        self.__test_columns_helper([two], [6, 8, 5])
        four.remove(1)
        self.__test_columns_helper([two], [6, 5, 5])

    def __test_columns_helper(self, rows: List[Row], target_lengths: List[int]):
        for row in rows:
            for i in range(len(row)):
                self.assertEqual(len(row.padded_field(i)), target_lengths[i])

    def test_insert(self):
        actual = Row(columns=[], fields=["one", "two", "three"])
        target = Row(columns=[], fields=["one", "two", "three", "four"])
        actual.append("four")
        self.assertEqual(actual, target)
        actual = Row(columns=[], fields=[])
        target = Row(columns=[], fields=["one"])
        actual.insert(0, "one")
        self.assertEqual(actual, target)
        actual = Row(columns=[], fields=["one", "three"])
        target = Row(columns=[], fields=["one", "two", "three"])
        actual.insert(1, "two")
        self.assertEqual(actual, target)

    def test_remove(self):
        actual = Row(columns=[], fields=["one", "two", "three", "four"])
        target = Row(columns=[], fields=["one", "two", "three"])
        self.assertRaises(Exception, lambda *args: actual.remove(4))
        actual.remove(3)
        self.assertEqual(actual, target)
        target = Row(columns=[], fields=["one", "three"])
        actual.remove(1)
        self.assertEqual(actual, target)
        target = Row(columns=[], fields=["three"])
        actual.remove(0)
        self.assertEqual(actual, target)

    def test_replace(self):
        actual = Row(columns=[], fields=["one", "two", "three"])
        target = Row(columns=[], fields=["one", "two", "3"])
        actual.replace(2, "3")
        self.assertEqual(actual, target)
        target = Row(columns=[], fields=["1", "two", "3"])
        actual.replace(0, "1")
        self.assertEqual(actual, target)

    def test_iter(self):
        actual = Row(columns=[], fields=["one", "two", "three"])
        target = "one    two    three"
        result = ''
        for field in actual:
            result += field
        self.assertEqual(result, target)

    def test_iter_complex(self):
        columns = []
        actual = Row(columns, fields=["one", "two", "three"])
        other = Row(columns, fields=["0123", "123", "0123456"])
        target = "one     two    three"
        result = ''
        for field in actual:
            result += field
        self.assertEqual(result, target)

    def test_getters(self):
        columns = []
        row = Row(columns, fields=["one", "two", "three"])
        Row(columns, fields=["0123", "123", "0123456"])
        self.assertEqual(len(row), 3)
        self.assertEqual(row.field(2), "three")
