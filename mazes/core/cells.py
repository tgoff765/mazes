from typing import Dict, List
from mazes.core.distances import Distances


class Cell:
    """
    Represents an individual cell of our maze
    """

    # Each cell should know where it is in the maze
    # Track what other cells are connected to this cell, as well as which cells lie N/E/S/W of it
    row: int
    column: int
    north: "Cell"
    east: "Cell"
    west: "Cell"
    south: "Cell"
    neighboring_cells: Dict["Cell", bool]

    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.neighboring_cells = {}

    def link(self, cell_to_link: "Cell", bidi: bool = True) -> None:
        """
        Link another cell to this one, and optionally bidirectionally link the cell we're about to link to this one
        """

        self.neighboring_cells[cell_to_link] = True

        if bidi:
            cell_to_link.neighboring_cells[self] = True

    def unlink(self, cell_to_unlink: "Cell", bidi: bool = True) -> None:
        """
        Unlink another cell to this one, and optionally bidirectionally unlink the cell we're about to unlink to this one
        """

        self.neighboring_cells[cell_to_unlink] = False

        if bidi:
            cell_to_unlink.neighboring_cells[self] = False

    def links(self) -> List["Cell"]:
        """
        Return all the cells linked to this cell
        """

        return [key for key in self.neighboring_cells.keys()]

    def is_linked(self, other_cell: "Cell") -> bool:
        """
        Returns T/F if the other_cell is linked to this one
        """

        return other_cell in self.neighboring_cells.keys()

    def neighbors(self) -> List["Cell"]:
        """
        Return each of the immediate neighbor cells to this cell, regardless if they are linked to cell or not
        """
        neighbors = []
        if self.north:
            neighbors.append(self.north)
        if self.south:
            neighbors.append(self.south)
        if self.east:
            neighbors.append(self.east)
        if self.west:
            neighbors.append(self.west)

        return neighbors

    def distances(self) -> "Distances":
        """
        Calculate the distances to each of the other cells in the grid from the current cell
        """
        # Create a new distances class starting with this cell
        distances = Distances(self)
        # Keep track of all the cells we want to visit and record the distance too, starting with this cell
        frontier = [self]

        while frontier:
            # List to hold the cells we'll consider on the next pass
            new_frontier = []

            # For every cell in the frontier and every linked cell for every cell..
            for cell in frontier:
                for linked_cell in cell.links():
                    # Check if we've already visited a cell, if we have continue
                    if distances.get_cell_distance(linked_cell) is not None:
                        continue
                    # Otherwise set cell distance to that unvistied cell as one more than the distance
                    # to the cell we're currently visiting
                    distances.set_cell_distance(
                        linked_cell, distances.get_cell_distance(cell) + 1
                    )
                    # Add linked_cell to visit on next pass
                    new_frontier.append(linked_cell)

            # Update frontier before next pass
            frontier = new_frontier

        return distances
