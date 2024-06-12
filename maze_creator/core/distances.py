from typing import Dict, List, Union


class Distances:
    """
    Takes a cell and calculates the distance to every other cell that it is linked to.
    """

    root: "Cell"
    distance_to_cells: Dict["Cell", int]  # Holds the distance from the root to the cell

    def __init__(self, cell: "Cell"):
        self.root = cell
        self.distance_to_cells = {
            self.root: 0
        }  # Instantiate a dict where the distance from the root to itself is 0

    def calc_distances(self):
        """
        Calculate the distances to each of the other cells in the grid from the current cell
        """
        # Keep track of all the cells we want to visit and record the distance too, starting with this cell
        frontier = [self.root]

        while frontier:
            # List to hold the cells we'll consider on the next pass
            new_frontier = []

            # For every cell in the frontier and every linked cell for every cell..
            for cell in frontier:
                # Skip blocked off cells
                if cell is None:
                    continue
                for linked_cell in cell.links():
                    # Check if we've already visited a cell, if we have continue
                    if self.get_cell_distance(linked_cell) is not None:
                        continue
                    # Otherwise set cell distance to that unvisited cell as one more than the distance
                    # to the cell we're currently visiting
                    self.set_cell_distance(linked_cell, self.get_cell_distance(cell) + 1)
                    # Add linked_cell to visit on next pass
                    new_frontier.append(linked_cell)

            # Update frontier before next pass
            frontier = new_frontier

    def get_cell_distance(self, cell: "Cell") -> Union[int, None]:
        """
        Get the distance from root to given cell
        """
        if cell in self.distance_to_cells.keys():
            return self.distance_to_cells[cell]
        else:
            return None

    def set_cell_distance(self, cell: "Cell", dist: int) -> None:
        """
        Set the distance from root to supplied cell
        """
        self.distance_to_cells[cell] = dist

    def get_all_cells(self) -> List["Cell"]:
        """
        Return a list of all the cells that we have recorded distances for
        """
        return list(self.distance_to_cells.keys())

    def max(self) -> tuple["Cell", int]:
        """
        Calculate the maximum cell from root
        """
        max_distance = 0
        max_cell = self.root

        for cell, distance in self.distance_to_cells.items():
            if distance > max_distance:
                max_distance = distance
                max_cell = cell

        return max_cell, max_distance

    def path_to(self, goal: "Cell") -> "Distances":
        """
        Use Dijkstra's algorithm to find a path from root to goal. Returns a distances mapping representing the
        shortest path to the goal
        """
        if goal is None:
            raise Exception("Cell doesn't exist or is blocked off")
        current = goal
        # Create a new distances object from root
        breadcrumbs = Distances(self.root)
        # Set the overall distance to goal
        breadcrumbs.set_cell_distance(current, self.distance_to_cells[current])
        # Work our way backwards starting from goal node
        while current != self.root:
            for neighbor in current.links():
                # If any of the neighbors' distance from root is shorter than current distance add that to our
                # distances obj
                if self.distance_to_cells[neighbor] < self.distance_to_cells[current]:
                    breadcrumbs.set_cell_distance(
                        neighbor, self.distance_to_cells[neighbor]
                    )
                    current = neighbor
                    break
        # Return breadcrumbs, end result should be a path of distances from root to goal that is as short as possible
        return breadcrumbs
