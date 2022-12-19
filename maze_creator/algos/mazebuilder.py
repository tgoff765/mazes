from abc import ABC, abstractmethod
from maze_creator.core.grid import DistanceGrid
from PIL import Image


class MazeBuilder(ABC):
    """
    Base ABC all maze building algorithms must implement
    """

    grid: DistanceGrid

    def __init__(self, **kwargs):
        self.grid = DistanceGrid(kwargs.get("rows", 10), kwargs.get("columns", 10))

    def __str__(self) -> str:
        """
        Delegate print method to grid
        """
        return self.grid.__str__()

    @abstractmethod
    def create_maze(self, **kwargs) -> DistanceGrid:
        """
        Applies the actual maze algorithm and mutates grid to hold final maze
        """
        pass

    def draw_maze(self, **kwargs) -> Image:
        return self.grid.draw(**kwargs)

    def solve(self, **kwargs) -> DistanceGrid:
        """
        Create a distance grid object of the created grid and find shortest path
        """
        # Calculate distances from starting node (default is path from upper NW corner to lower SE corner)
        self.grid.find_path_to(
            kwargs.get("start_row", 0),
            kwargs.get("start_col", 0),
            kwargs.get("end_row", self.grid.rows - 1),
            kwargs.get("end_col", 0),
        )
        return self.grid
