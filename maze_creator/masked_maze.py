from maze_creator.algos.aldousbroder import AldousBroder
from maze_creator.algos.huntandkill import HuntAndKill
from maze_creator.algos.recursivebacktracker import RecursiveBackTracker
from maze_creator.algos.wilson import Wilson
from maze_creator.core.mask import Mask
from maze_creator.grids.masked_grid import MaskedGrid
from maze_creator.views.distances_view import DistancesView
from maze_creator.views.path_finder_view import PathFinderView
from maze_creator.visuals.maze_image_creator import MazeImageCreator, ColorChoice


# TODO: Combine this with Maze class and determine which algorithms still work with masking
class MaskedMaze:

    def __init__(self, mask, type):
        self.grid = MaskedGrid(mask)
        self.rows = mask.rows
        self.columns = mask.columns

        if type == "recursive":
            self.grid = RecursiveBackTracker.create_maze(self.grid)
        elif type == "aldous":
            self.grid = AldousBroder.create_maze(self.grid)
        elif type == "binary":
            raise Exception("Masked grids can't use binary algorithm.")
        elif type == "hunt":
            self.grid = HuntAndKill.create_maze(self.grid)
        elif type == "recursive":
            self.grid = RecursiveBackTracker.create_maze(self.grid)
        elif type == "side":
            raise Exception("Masked grids can't use sidewinder algorithm.")
        elif type == "wilson":
            self.grid = Wilson.create_maze(self.grid)
        else:
            raise Exception("Maze type not recognized")

    def __str__(self):
        return self.grid.__str__()


if __name__ == "__main__":

    mask = Mask.from_image("../docs/masks/test.png")

    test = MaskedMaze(mask, "wilson")
    og = MazeImageCreator(test)
    og.draw()

    distances_view = DistancesView(test, 0, 0)
    image2 = MazeImageCreator(
        distances_view, "distance", color_choice=ColorChoice.DARKGREEN
    )
    image2.draw()
