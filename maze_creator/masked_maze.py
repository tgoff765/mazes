from maze_creator.algos.recursivebacktracker import RecursiveBackTracker
from maze_creator.core.mask import Mask
from maze_creator.grids.masked_grid import MaskedGrid
from maze_creator.visuals.maze_image_creator import MazeImageCreator


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
    mask.bits[0][0] = False
    mask.bits[1][1] = False
    mask.bits[2][2] = False
    mask.bits[3][3] = False

    test = MaskedMaze(mask, "Recursive")
    og = MazeImageCreator(test)
    og.draw()
