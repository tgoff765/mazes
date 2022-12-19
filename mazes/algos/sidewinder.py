from mazes.core.grid import DistanceGrid
from random import choice, uniform
from mazes.algos.mazebuilder import MazeBuilder


class SideWinder(MazeBuilder):
    def create_maze(self, **kwargs) -> DistanceGrid:
        """
        Visit every cell in the gird and attach the eastern cell so long as the random number generated falls below the
        bias. After we hit our first miss, we have created a "run" (aka a group) of cells and then must pick a northern
        cell at random to link to our run.

        Note that a run is automatically closed out whenever it reaches the end of a row.

        When we reach the northernmost row, we connect the entire top row making one connected run. Thus, this algorithm
        will always create mazes where the top row is connected (in the default orientation).

        Called the sidewinder algorithm because a solution can be found to the maze by winding from bottom to the top
        of the maze looking for the northern cell connection since at the very least every row must be connected to
        its neighboring top row by at least one cell.
        """
        for row in self.grid.each_row():
            # Create an empty run for each row
            run = []

            for cell in row:
                run.append(cell)
                # Indicator flags
                at_eastern_boundary = cell.east is None
                at_northern_boundary = cell.north is None
                # Close out the current run of we're at eastern_boundary or not at north and our random number
                # flipped tells us to
                should_close_out = at_eastern_boundary or (
                    not at_northern_boundary
                    and kwargs.get("horizontal_bias", 0.5) < uniform(0, 1)
                )

                if should_close_out:
                    # Pick a random cell in our current run
                    member = choice(run)
                    # Check one more time to see if it has northern neighbor, this is to prevent an error
                    # when we reach the north-eastern most corner (in default orientation)
                    if member.north is not None:
                        member.link(member.north)
                    # Start a new run
                    run = []
                else:
                    # If we're still within a run just link current cell to its eastern neighbor
                    cell.link(cell.east)
        return self.grid
