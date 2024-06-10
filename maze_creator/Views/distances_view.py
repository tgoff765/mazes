from typing import List

from maze_creator.core.cells import Cell
from maze_creator.core.distances import Distances


# Could this be broken out into 2 sepearte classes?
class DistancesView:
    """
    Given a grid and cell coordinates, colors all cells according how far they are from the starting cell
    """

    grid: List[List["Cell"]]
    cell: Cell
    distances: Distances
    max: int
    columns: int
    rows: int

    def __init__(self, maze, row: 0, column: 0):
        self.grid = maze.grid
        self.cell = self.grid[row, column]
        self.calculate_distances(self.cell)

    def calculate_distances(self, cell) -> None:
        """
        Calculate all the distances from the supplied cell
        """
        # Calculate all the distances from the target cell to everywhere else in the graph
        self.distances = Distances(cell)
        self.distances.calc_distances()
        _, self.max = self.distances.max()
