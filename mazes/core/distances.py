from typing import Dict, List, Union


class Distances:
    """
    Holds distances from a root (origin cell) to every other cell in the maze
    """

    root: "Cell"
    cells: Dict["Cell", int]  # Holds the distance from the root to the cell

    def __init__(self, cell: "Cell"):
        self.root = cell
        self.cells = {
            self.root: 0
        }  # Instantiate a dict where the distance from the root to itself is 0

    def get_cell_distance(self, cell: "Cell") -> Union[int, None]:
        """
        Get the distance from root to given cell
        """
        if cell in self.cells.keys():
            return self.cells[cell]
        else:
            return None

    def set_cell_distance(self, cell: "Cell", dist: int) -> None:
        """
        Set the distance from root to supplied cell
        """
        self.cells[cell] = dist

    def get_all_cells(self) -> List["Cell"]:
        """
        Return a list of all the cells that we have recorded distances for
        """
        return list(self.cells.keys())

    def path_to(self, goal: "Cell") -> "Distances":
        """
        Use Dijkstra's algorithm to find a path from root to goal. Returns a distances mapping representing the
        shortest path to the goal
        """
        current = goal
        # Create a new distances object from root
        breadcrumbs = Distances(self.root)
        # Set the overall distance to goal
        breadcrumbs.set_cell_distance(current, self.cells[current])
        # Work our way backwards starting from goal node
        while current != self.root:
            for neighbor in current.links():
                # If any of the neighbors' distance from root is shorter than current distance add that to our
                # distances obj
                if self.cells[neighbor] < self.cells[current]:
                    breadcrumbs.set_cell_distance(neighbor, self.cells[neighbor])
                    current = neighbor
                    break
        # Return breadcrumbs, end result should be a path of distances from root to goal that is as short as possible
        return breadcrumbs

    def max(self) -> tuple["Cell", int]:
        """
        Calculate the maximum cell from root
        """
        max_distance = 0
        max_cell = self.root

        for (cell, distance) in self.cells.items():
            if distance > max_distance:
                max_distance = distance
                max_cell = cell

        return max_cell, max_distance
