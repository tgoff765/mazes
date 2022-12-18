from src.core.grid import DistanceGrid
from random import choice
from src.algos.mazebuilder import MazeBuilder


class Wilson(MazeBuilder):

    def create_maze(self, **kwargs) -> DistanceGrid:
        """
        Generate a maze by marking a cell visited, then visiting a random path in the maze. We erase and loops our
        path may create and once we find a visited cell we carve a path to it. Note that algorithm is unbiased like
        Aldous-Broder and it can also take a similarly long time to run (since its a random walk). Runtime wise, this
        algorithm starts slow, since it has to find visited cells to carve paths to, but picks up in speed as more
        cells become visited (hence making it easier to carve paths).
        """
        # Initialize a list of unvisited cells from the grid
        unvisited = [cell for cell in self.grid.each_cell()]

        # Pick a random cell from the list and mark it visited by deleting from list
        first = choice(unvisited)
        unvisited.remove(first)

        while len(unvisited) > 0:
            # Choose a cell at random and start a prospective path
            cell = choice(unvisited)
            path = [cell]

            # While our cell is unvisited (loop erasure section)
            while cell in unvisited:
                # Take a random cell from our neighbors
                cell = choice(cell.neighbors())
                # Check to see if we've formed a loop yet, if we have erase it.
                if cell in path:
                    # If we've formed a loop, truncate path up until the cell first appeared
                    # Add 1 to position so that it's included in the truncated slice
                    position = path.index(cell)
                    path = path[0:position + 1]
                else:
                    # Otherwise just append the cell to the path
                    path.append(cell)

            # Once we hit a visited cell, we move to the path carving stage
            # Iterate over each cell in our path (subtracting 1 from range so we stop 1 shy of the last element)
            for i in range(len(path) - 1):
                # Link every element to its next neighbor and then delete it from our unvisited cell
                path[i].link(path[i+1])
                unvisited.remove(path[i])

        return self.grid
