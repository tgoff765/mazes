from maze_creator.algos.recursivebacktracker import RecursiveBackTracker
from maze_creator.masks.mask import Mask
from maze_creator.masks.masked_grid import MaskedGrid
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
    mask = Mask(10, 10)
    mask.bits[0][2] = False
    mask.bits[0][9] = False
    mask.bits[5][5] = False

    test = MaskedMaze(mask, "Recursive")
    og = MazeImageCreator(test)
    og.draw()
