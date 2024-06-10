import unittest

from maze_creator.core.cells import Cell
from maze_creator.core.distances import Distances


class TestDistances(unittest.TestCase):
    def setUp(self):
        self.cell = Cell(0, 0)

    def test_distance_horizontal(self):
        cell2 = Cell(0, 1)
        cell3 = Cell(0, 2)
        cell4 = Cell(0, 3)
        cell2.link(self.cell)
        cell3.link(cell2)
        cell4.link(cell3)
        distances = Distances(self.cell)

        expected = 3
        actual = distances.get_cell_distance(cell4)
        self.assertEqual(expected, actual)

    def test_distance_vertical(self):
        cell2 = Cell(1, 0)
        cell3 = Cell(2, 0)
        cell4 = Cell(3, 0)
        cell2.link(self.cell)
        cell3.link(cell2)
        cell4.link(cell3)
        distances = Distances(self.cell)

        expected = 3
        actual = distances.get_cell_distance(cell4)
        self.assertEqual(expected, actual)

    def test_distance_diagonal(self):
        cell2 = Cell(0, 1)
        cell3 = Cell(0, 2)
        cell4 = Cell(1, 1)
        cell5 = Cell(1, 2)
        cell2.link(self.cell)
        cell3.link(cell2)
        cell4.link(cell2)
        cell5.link(cell3)
        cell5.link(cell4)

        distances = Distances(self.cell)

        expected = 3
        actual = distances.get_cell_distance(cell5)
        self.assertEqual(expected, actual)
