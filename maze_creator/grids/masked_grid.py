from maze_creator.algos.recursivebacktracker import RecursiveBackTracker
from maze_creator.core.cells import Cell
from maze_creator.grids.grid import Grid
from maze_creator.core.mask import Mask


class MaskedGrid(Grid):

    def __init__(self, mask):
        self.mask = mask
        super().__init__(mask.rows, mask.columns)

    def _prepare_grid(self):
        """
        Check each cell in the grid, and if it's not set in the corresponding mask bit, set the cell to None.
        This overrides the prepare grid method in the base class.
        """
        self.grid = []

        current_row = 0
        current_column = 0

        while current_row < self.rows:
            self.grid.append([])
            while current_column < self.columns:
                if self.mask[current_row, current_column]:
                    self.grid[current_row].append(Cell(current_row, current_column))
                else:
                    self.grid[current_row].append(None)
                current_column += 1

            current_column = 0
            current_row += 1

    def random_cell(self):
        row, col = self.mask.random_location()
        return self.grid[row][col]

    def size(self):
        return self.mask.count()


if __name__ == "__main__":
    mask = Mask.from_txt("../../docs/masks/olaf.txt")
    test = MaskedGrid(mask)
    test2 = RecursiveBackTracker.create_maze(test)
    print(test2)
