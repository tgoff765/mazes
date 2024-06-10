from typing import Union

from maze_creator.core.cells import Cell
from maze_creator.core.distances import Distances


class PathFinderView:
    """
    Find the path between two different cells in a maze
    """

    distances: Union[Distances, None]

    path_distance = Union[int, None]

    def __init__(
        self,
        maze,
        starting_cell_row,
        starting_cell_column,
        ending_cell_row,
        ending_cell_column,
    ):
        self.grid = maze.grid
        self.starting_cell = self.grid[starting_cell_row, starting_cell_column]
        self.distances = Distances(self.starting_cell)
        self.distances.calc_distances()
        self.ending_cell = self.grid[ending_cell_row, ending_cell_column]
        self.path = self.distances.path_to(self.ending_cell)
        self.path_distance = self.distances.get_cell_distance(self.ending_cell)

    def __str__(self) -> str:
        """
        Provide a pretty ASCII representation of the grid
        """
        # Draw the top border
        output = "+" + "---+" * self.grid.columns + "\n"

        for row in self.grid.each_row():
            # Because every cell generates its own southern and eastern borders we don't have to worry about
            # western or northern borders
            top = "|"  # Start of the eastern border
            bottom = "+"  # Start of the southern border

            for cell in row:
                # Skip cells that are masked
                if cell is None:
                    continue

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

    def contents_of_cell(self, cell) -> str:
        """
        Helper function to pick what each cell should be displayed as in string representation.
        """
        if self.path and self.path.get_cell_distance(cell) is not None:
            # Use asterix to record spots in
            return "*"
        else:
            return " "
