from random import choice

from maze_creator.core.grid import DistanceGrid
from maze_creator.core.mazebuilder import MazeBuilder


class RecursiveBackTracker(MazeBuilder):
    """
    Visit random cells in a maze, pushing each cell onto a stack until we reach a cell that has no unvisited neighbors.
    We then pop cells off the maze (aka backtrack) until we can find an unvisited neighbor and proceed making a path.
    The algorithm finishes once the stack is empty.
    Note: this is essentially depth first search.
    Will produce mazes very similar to huntandkill, the trade-off is that this is more memory-intensive but faster
    since each cell is guaranteed to be visited exactly twice.
    """

    def create_maze(self, **kwargs) -> DistanceGrid:
        # Initialize the stack with random cell to start visiting on
        stack = [self.grid.random_cell()]

        while len(stack) > 0:
            # Examine current item at the top of the stack and check to see if it has any unvisited neighbors
            current = stack[-1]
            unvisited_neighbors = list(
                filter(lambda n: len(n.links()) == 0, current.neighbors())
            )
            # If there are no unvisited neighbors pop another cell of the stack, otherwise choose another
            # random unvisited neighbor to visit
            if len(unvisited_neighbors) == 0:
                stack.pop()
            else:
                neighbor = choice(unvisited_neighbors)
                current.link(neighbor)
                stack.append(neighbor)

        return self.grid
