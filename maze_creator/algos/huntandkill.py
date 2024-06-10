from random import choice
from typing import Union

from maze_creator.core.cells import Cell
from maze_creator.core.grid import Grid


class HuntAndKill:
    @staticmethod
    def create_maze(grid) -> Grid:
        """
        Biased algorithm that creates a path that from unvisited neighbors. When it can't do that, it then
        looks for a random cell to connect it to and then proceeds from there creating a path. Tends to create
        a maze with a lot of winding paths and few dead ends.
        """
        # Pick a random cell to start the algorithm from
        current: Union[Cell, None] = grid.random_cell()

        while current:
            # Filter the list of neighbors to those who have 0 neighbors
            unvisited_neighbors = list(
                filter(lambda n: len(n.links()) == 0, current.neighbors())
            )

            # Hunt
            # If there are any unvisited neighbors, pick one at random, link to our current cell and set current to
            # neighbor
            if unvisited_neighbors:
                neighbor = choice(unvisited_neighbors)
                current.link(neighbor)
                current = neighbor
            else:
                # Kill
                # Reset current
                current = None
                # Look for a cell in grid to connect to our current path
                for cell in grid.each_cell():
                    # Filter neighbors to ones with at least one link
                    visited_neighbors = list(
                        filter(lambda n: len(n.links()) > 0, cell.neighbors())
                    )
                    # Look for cell that is not current linked but who has at least one neighbor
                    # Set current to that cell and link to one of its random neighbors
                    if len(cell.links()) == 0 and len(visited_neighbors) > 0:
                        current = cell
                        neighbor = choice(visited_neighbors)
                        current.link(neighbor)
                        break

        # If we can't find a cell that satisfies the criteria, we are done and return
        return grid
