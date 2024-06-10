import unittest
from maze_creator.core.cells import Cell


class TestCells(unittest.TestCase):
    def setUp(self):
        pass

    def test_single_cell_has_no_neighbors(self):
        test_cell = Cell(1, 1)

        expected = 0
        actual = len(test_cell.links())
        message = f"Expected {expected} number of neighbors, got {actual}"
        self.assertEqual(expected, actual, message)

    def test_cell_with_multiple_neighbors(self):
        test_cell = Cell(1, 1)
        test_cell_2 = Cell(1, 2)
        test_cell_3 = Cell(2, 1)
        test_cell.link(test_cell_2)
        test_cell.link(test_cell_3)

        expected = 2
        actual = len(test_cell.links())
        message = f"Expected {expected} number of neighbors, got {actual}"
        self.assertEqual(expected, actual, message)

    def test_link_cells(self):
        test_cell = Cell(1, 1)
        test_cell_2 = Cell(2, 2)
        test_cell.link(test_cell_2)

        self.assertTrue(test_cell.is_linked(test_cell_2))
        self.assertTrue(test_cell_2.is_linked(test_cell))

    def test_unlink_cells(self):
        test_cell = Cell(1, 1)
        test_cell_2 = Cell(2, 2)
        test_cell.link(test_cell_2)
        test_cell.unlink(test_cell_2)
        self.assertFalse(test_cell.is_linked(test_cell_2))
