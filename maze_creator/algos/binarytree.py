from random import uniform

from maze_creator.core.grid import Grid


class BinaryTree:
    @staticmethod
    def create_maze(grid, horizontal_bias: float = 0.5) -> Grid:
        """
        Generate a maze by walking through every cell in the grid and at each cell linking either the northern or
        the eastern cell to the one currently visited.

        When we reach a cell we cannot link a side to (e.g. on the eastern edge of the grid there are no more eastern cells
        we can link), this algorithm will always open the other side.

        Because of this rule, this algorithm creates maze_creator that have a bias towards NE direction and will always have
        a completely linked eastern column and northern row (in default orientation)
        """

        for cell in grid.each_cell():

            rand_float = uniform(0, 1)
            # If we're in the upper right-hand corner we can't connect anything
            if not cell.north and not cell.east:
                pass
            # If we are in the easternmost column (but not upper corner), always connect northern cell
            elif not cell.east:
                cell.link(cell.north)
            # If we're in the northernmost row (but not upper corner), always connect the eastern cell
            elif not cell.north:
                cell.link(cell.east)
            # Otherwise, connect the eastern cell if our random number falls below the horizontal bias, and connect
            # the northern cell if it does not
            elif cell.east and rand_float < horizontal_bias:
                cell.link(cell.east)
            else:
                cell.link(cell.north)

        return grid
