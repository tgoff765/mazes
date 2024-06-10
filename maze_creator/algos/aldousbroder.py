from abc import ABC, abstractmethod
from random import choice

from maze_creator.core.grid import Grid


class AldousBroder(ABC):
    @staticmethod
    def create_maze(grid) -> Grid:
        """
        Random walk algorithm, start with a random cell,
        pick a random neighbor and if it hasn't already been
        visited link it with the previous cell.
        """
        # Start on a random cell
        cell = grid.random_cell()
        # Calculate the number of cells left unvisited
        # (subtract 1 since we consider starting grid as already visited)
        unvisited = grid.size() - 1

        while unvisited > 0:
            # Pick a random neighbor of current cel
            neighbor = choice(cell.neighbors())

            # If that neighbor has no links yet,
            # link it to current cell and decrement unvisited
            if len(neighbor.links()) == 0:
                cell.link(neighbor)
                unvisited -= 1

            cell = neighbor

        return grid
