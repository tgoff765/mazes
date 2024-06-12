from maze_creator.algos.recursivebacktracker import RecursiveBackTracker
from maze_creator.core.cells import Cell
from maze_creator.core.grid import Grid
from maze_creator.masks.mask import Mask


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

        # for row in self.grid:
        #     for c in row:
        #         # Remove is problematic here because it shifts everything over, do we just want to insert an empty list?
        #         if not self.mask.bits[row_num][col_num]:
        #             self.grid[row_num][col_num] = None
        #         col_num += 1
        #     col_num = 0
        #     row_num += 1

    def random_cell(self):
        row, col = self.mask.random_location()
        return self.grid[row][col]

    def size(self):
        return self.mask.count()


if __name__ == "__main__":
    grid = Grid(4, 4)
    mask = Mask(4, 4)
    mask.bits[0][2] = False
    mask.bits[1][1] = False
    test = MaskedGrid(mask)
    print(test.grid)
    test2 = RecursiveBackTracker.create_maze(test)
    print(test2)
