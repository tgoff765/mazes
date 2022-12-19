from mazes.algos.mazebuilder import MazeBuilder
from mazes.algos.binarytree import BinaryTree
from mazes.algos.sidewinder import SideWinder
from mazes.algos.aldousbroder import AldousBroder
from mazes.algos.huntandkill import HuntAndKill
from mazes.algos.wilson import Wilson
from enum import Enum
from mazes.core.grid import ColorGrid, DistanceGrid
from PIL import Image


class MazeType(Enum):
    BINARY = 1
    SIDEWINDER = 2
    ALDOUSBRODER = 3
    WILSON = 4
    HUNTANDKILL = 5


class Maze:
    """
    Main driver for mazes. All client code should call this when creating and displaying mazes.
    """

    maze_type: str
    maze_builder: MazeBuilder
    maze: DistanceGrid
    maze_image: Image

    def __init__(self, maze_type: MazeType, **kwargs):
        """
        Specify maze type + series of optional configuration properties
        # Maze properties
        :keyword: columns: int = # of columns in maze (default 10)
        :keyword: rows: int  = # of rows in maze (default 10)
        # Algorithm properties
        :keyword: horizontal_bias: float = proportion of time the algorithm should
                                            link eastern cell vs northern cell (default 0.5).
                                            Only applicable to binary and sidewinder algorithms.
        # Draw properties
        :keyword: canvas_color: (int, int, int) = RGB Color of background (default white)
        :keyword: line_color: (int, int, int) = RGB Color of maze lines (default black)
        :keyword: cell_size: int = Num of pixels used per maze cell (default 10)
        :keyword: line_thickness: int = Num of pixels user per maze line (default 1)

        # Solve properties
        :keyword: start_row: int, start_col: int = Starting point for path (default NW corner)
        :keyword: end_row: int, end_col: int = Ending point for path (default SW corner)
        """

        maze_map = {
            MazeType.BINARY: BinaryTree,
            MazeType.SIDEWINDER: SideWinder,
            MazeType.ALDOUSBRODER: AldousBroder,
            MazeType.WILSON: Wilson,
            MazeType.HUNTANDKILL: HuntAndKill,
        }

        self.maze_builder = maze_map.get(maze_type)(**kwargs)
        self._create(**kwargs)

    def __str__(self):
        return self.maze.__str__()

    def _create(self, **kwargs) -> None:
        self.maze = self.maze_builder.create_maze(**kwargs)

    def draw(self, **kwargs) -> None:
        """
        Draw current representation of maze
        """
        self.maze_image = self.maze_builder.draw_maze(**kwargs)
        self.maze_image.show()

    def solve(self, **kwargs) -> DistanceGrid:
        """
        Return a string representation of the solved maze. Each time this is called a new path is generated.
        """
        return self.maze_builder.solve(**kwargs)

    def analyze(self, **kwargs) -> None:
        """
        Returns a colorgrid which when drawn colors in cells by how far in distance they are from the target cell
        Note: This does not edit the maze object, it returns a seperate view
        """
        cg = ColorGrid(
            self.maze, kwargs.get("start_row", 0), kwargs.get("start_col", 0)
        ).draw(**kwargs)
        cg.show()
