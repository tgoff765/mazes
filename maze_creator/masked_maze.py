from maze_creator.algos.recursivebacktracker import RecursiveBackTracker
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

        if type == "Recursive":
            self.grid = RecursiveBackTracker.create_maze(self.grid)

    def __str__(self):
        return self.grid.__str__()


if __name__ == "__main__":
    mask = Mask(20, 20)
    mask.bits[1][1] = False
    mask.bits[2][2] = False
    mask.bits[3][3] = False

    test = MaskedMaze(mask, "Recursive")
    og = MazeImageCreator(test)
    og.draw()

    distances_view = DistancesView(test, 19, 19)
    image2 = MazeImageCreator(
        distances_view, "distance", color_choice=ColorChoice.DARKGREEN
    )
    image2.draw()
