from core.grid import Grid
from algos.aldousbroder import AldousBroder
from algos.binarytree import BinaryTree
from algos.huntandkill import HuntAndKill
from algos.recursivebacktracker import RecursiveBackTracker
from algos.sidewinder import SideWinder
from algos.wilson import Wilson
from maze_creator.views.path_finder_view import PathFinderView
from maze_creator.views.distances_view import DistancesView
from visuals.maze_image_creator import MazeImageCreator


class Maze:
    """
    A maze is fundamentally a grid + an algorithm applied on top.
    """

    def __init__(
        self,
        rows: int = 10,
        columns: int = 10,
        type: str = "Binary",
        horizontal_bias: float = 0.5,
    ):
        self.grid = Grid(rows, columns)

        if type == "Aldous":
            self.grid = AldousBroder.create_maze(self.grid)
        elif type == "Binary":
            self.grid = BinaryTree.create_maze(self.grid, horizontal_bias)
        elif type == "Hunt":
            self.grid = HuntAndKill.create_maze(self.grid)
        elif type == "Recursive":
            self.grid = RecursiveBackTracker.create_maze(self.grid)
        elif type == "Side":
            self.grid = SideWinder.create_maze(self.grid, horizontal_bias)
        else:
            self.grid = Wilson.create_maze(self.grid)

    def __str__(self):
        return self.grid.__str__()


if __name__ == "__main__":
    maze = Maze(50, 50, "Hunt")
    og = MazeImageCreator(maze)
    og.draw()

    path_view = PathFinderView(maze, 0, 0,49,49)
    image = MazeImageCreator(maze=path_view, type ="path")
    image.draw()

    distances_view = DistancesView(maze, 0, 40)
    image2 = MazeImageCreator(distances_view, "distance")
    image2.draw(canvas_color=(124,64,12))

    image3 = MazeImageCreator(maze, "openings")
    image3.draw()
