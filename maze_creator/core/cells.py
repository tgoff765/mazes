from typing import Dict, List


class Cell:
    """
    Cells represent an individual tile in a maze. Cells know about their neighbors and are optionally linked
    to each of their neighbors (i.e. there's a passage between them).
    """

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

    def __str__(self) -> str:
        return f"Cell @ [row:{self.row}, col:{self.column}]"

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

        return self.neighboring_cells.get(other_cell, False)

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
