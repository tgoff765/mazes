from random import randint
from typing import Generator, List, Union

from maze_creator.core.cells import Cell


class Grid:
    """
    Grid is a list of lists of cells
    """

    # Dimensions of the grid + containing 2D array of cells
    rows: int
    columns: int
    grid: List[List["Cell"]]

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self._prepare_grid()
        self._configure_cells()

    def contents_of_cell(self, cell) -> str:
        """
        Pick what each cell should be displayed as in string representation
        """
        return " "

    def __str__(self) -> str:
        """
        Provide a pretty ASCII representation of the grid
        """
        # Draw the top border
        output = "+" + "---+" * self.columns + "\n"

        for row in self.each_row():
            # Because every cell generates its own southern and eastern borders we don't have to worry about
            # western or northern borders
            top = "|"  # Start of the eastern border
            bottom = "+"  # Start of the southern border

            for cell in row:
                # Every cell is three spaces wide
                body = f" {self.contents_of_cell(cell)} "
                # If the cell is linked to the east add a space (open passage) otherwise add a pipe to represent wall
                east_boundary = (
                    " "
                    if isinstance(cell, Cell)
                    and hasattr(cell, "east")
                    and cell.is_linked(cell.east)
                    else "|"
                )
                top += body + east_boundary
                # If the cell is linked to the south add three spaces (open passage)
                # otherwise add vertical bars for wall
                south_boundary = (
                    "   "
                    if isinstance(cell, Cell)
                    and hasattr(cell, "south")
                    and cell.is_linked(cell.south)
                    else "---"
                )
                corner = "+"
                bottom += south_boundary + corner

            # Update output after each row has been visited
            output += top + "\n"
            output += bottom + "\n"

        return output

    def __getitem__(self, tup) -> Union["Cell", None]:
        """
        Return a slice of the underlying grid only if the rows and columns are non-negative, otherwise return None
        This way we can access the Cell of a Grid by Grid[row, column]
        """
        y, x = tup
        if 0 <= y <= (self.rows - 1) and 0 <= x <= (self.columns - 1):
            return self.grid[y][x]
        return None

    def _prepare_grid(self) -> None:
        """
        Create a 2D array of row * column of Cells and set neighbors for each sell
        """
        self.grid = [
            [Cell(row, column) for column in range(self.columns)]
            for row in range(self.rows)
        ]

    def _configure_cells(self):

        for row in self.grid:
            for c in row:
                if c is not None:
                    row, column = c.row, c.column

                    # See __getitem__ for details on how this is implemented
                    c.north = self[row - 1, column]
                    c.south = self[row + 1, column]
                    c.east = self[row, column + 1]
                    c.west = self[row, column - 1]

    # Utility functions
    def random_cell(self) -> "Cell":
        """
        Return a random cell from the Grid
        """
        return self.grid[randint(0, self.rows - 1)][randint(0, self.columns - 1)]

    def size(self) -> int:
        """
        Return size of the maze defined as the number of rows * number of columns
        """
        return self.rows * self.columns

    # Iterators
    def each_row(self) -> Generator[List["Cell"], None, None]:
        """
        Generator function for each row
        """
        for row in self.grid:
            yield row

    def each_cell(self) -> Generator["Cell", None, None]:
        """
        Generator function for each cell
        """
        for row in self.grid:
            for cell in row:
                if isinstance(cell, Cell):
                    yield cell


if __name__ == "__main__":
    test = Grid(10, 10)
    print(test)
