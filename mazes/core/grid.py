from typing import Generator, List, Union
from random import randint
from mazes.core.cells import Cell
from mazes.core.distances import Distances
from PIL import Image, ImageDraw


class Grid:
    """
    Wrapper class for a 2D array of cells
    """

    # Dimensions of the grid + containing 2D array of cells
    rows: int
    columns: int
    grid: List[List["Cell"]]

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.prepare_grid()
        self.configure_grid()

    def __getitem__(self, tup) -> Union["Cell", None]:
        """
        Return a slice of the underlying grid only if the rows and columns are non-negative, otherwise return None
        This way we can access the Cell of a Grid by Grid[row, column]
        """
        y, x = tup
        if 0 <= y <= (self.rows - 1) and 0 <= x <= (self.columns - 1):
            return self.grid[y][x]
        return None

    def contents_of_cell(self, cell) -> str:
        """
        Pick what each cell should be displayed as in string representation
        """
        return " "

    def background_color_for(self, cell) -> None:
        """
        Pick what the background color for each cell should be in the image
        """
        return None

    def __str__(self) -> str:
        """
        Provide a pretty ASCII representation of the grid
        """
        # Draw the top border
        output = "+" + "---+" * self.columns + "\n"

        for row in self.each_row():
            # Because every cell generates its own southern and eastern borders we don't have to worry about
            # western or northern borders
            top = "|"  # Start of the eastern border
            bottom = "+"  # Start of the southern border

            for cell in row:
                # Every cell is three spaces wide
                body = f" {self.contents_of_cell(cell)} "
                # If the cell is linked to the east add a space (open passage) otherwise add a pipe to represent wall
                east_boundary = " " if cell.is_linked(cell.east) else "|"
                top += body + east_boundary
                # If the cell is linked to the south add three spaces (open passage)
                # otherwise add vertical bars for wall
                south_boundary = "   " if cell.is_linked(cell.south) else "---"
                corner = "+"
                bottom += south_boundary + corner

            # Update output after each row has been visited
            output += top + "\n"
            output += bottom + "\n"

        return output

    def prepare_grid(self) -> None:
        """
        Create a 2D array of row * column of Cells
        """
        self.grid = [
            [Cell(row, column) for column in range(self.columns)]
            for row in range(self.rows)
        ]

    def configure_grid(self) -> None:
        """
        Loop through and configure immediate neighbors of cells.
        """
        for row in self.grid:
            for c in row:
                row, column = c.row, c.column

                # See __getitem__ for details on how this is implemented
                c.north = self[row - 1, column]
                c.south = self[row + 1, column]
                c.east = self[row, column + 1]
                c.west = self[row, column - 1]

    def random_cell(self) -> "Cell":
        """
        Return a random cell from the Grid
        """
        return self.grid[randint(0, self.rows - 1)][randint(0, self.columns - 1)]

    def size(self) -> int:
        """
        Return size of the maze defined as the number of rows * number of columns
        """
        return self.rows * self.columns

    def each_row(self) -> Generator[List["Cell"], None, None]:
        """
        Generator function for each row
        """
        for row in self.grid:
            yield row

    def each_cell(self) -> Generator["Cell", None, None]:
        """
        Generator function for each cell
        """
        for row in self.grid:
            for cell in row:
                yield cell

    def draw(self, **kwargs) -> Image:
        """
        Draw grid to canvas using the Pillow Library
        Note that a weakness of this rendering is that line width is drawn inside cells (instead of as a seperate grid)
        which means that if line_width is large enough it'll draw over the cell.
        In a future edit will need to disentangle the gridlines and the cells.
        In general, I'd recommend keeping line_thickness 10% the size of cell_size or less.
        """
        # Given supplied cell size in pixels construct the image canvas
        # Set parameters
        cell_size = kwargs.get("cell_size", 100)
        canvas_color = kwargs.get("canvas_color", (255, 255, 255))
        line_color = kwargs.get("line_color", (0, 0, 0))
        line_thickness = kwargs.get("line_thickness", 10)

        img_width = cell_size * self.columns
        img_height = cell_size * self.rows
        im = Image.new("RGB", (img_width + 1, img_height + 1), canvas_color)

        # Create a drawable version of the image
        draw = ImageDraw.Draw(im)

        # Draw each of the cells onto the image
        for row in self.grid:
            # Iterate through each mode, one iteration to loop through backgrounds, another to do cell walls
            for mode in ["backgrounds", "walls"]:
                for cell in row:
                    # Calc the northwest and southeast corner points, accounting for
                    x1 = cell.column * cell_size
                    y1 = cell.row * cell_size
                    x2 = (cell.column + 1) * cell_size
                    y2 = (cell.row + 1) * cell_size

                    if mode == "backgrounds":
                        color = self.background_color_for(cell)
                        if color:

                            western_boundary = x1
                            eastern_boundary = x2
                            northern_boundary = y1
                            southern_boundary = y2

                            # Need to adjust for line boundaries here, as far as I can tell, PIL will set the line
                            # at the midpoint of the line width, which is why we're using 0.5 here

                            if not cell.north or not cell.is_linked(cell.north):
                                northern_boundary += 0.5 * line_thickness

                            if not cell.west or not cell.is_linked(cell.west):
                                western_boundary += 0.5 * line_thickness

                            if not cell.is_linked(cell.south):
                                southern_boundary -= 0.5 * line_thickness

                            if not cell.is_linked(cell.east):
                                eastern_boundary -= 0.5 * line_thickness

                            draw.rectangle(
                                (
                                    (western_boundary, northern_boundary),
                                    (eastern_boundary, southern_boundary),
                                ),
                                color,
                                color,
                            )
                    else:
                        # Since every cell draws its southern and eastern borders, we only have to
                        # draw northern and western borders if the cell has no neighbor in that direction
                        if not cell.north:
                            draw.line(((x1, y1), (x2, y1)), line_color, line_thickness)

                        if not cell.west:
                            draw.line(((x1, y1), (x1, y2)), line_color, line_thickness)

                        # Every cell draws its own southern and eastern borders unless it is linked to that neighbor
                        if not cell.is_linked(cell.south):
                            draw.line(((x1, y2), (x2, y2)), line_color, line_thickness)

                        if not cell.is_linked(cell.east):
                            draw.line(((x2, y1), (x2, y2)), line_color, line_thickness)

        return im


class DistanceGrid(Grid):
    """
    Subclass of grid that calculates distances from a root node using Dijkstra's method given an already configured grid
    """

    distances: Distances
    rows: int
    columns: int
    grid: List[List["Cell"]]

    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.distances = None

    def calc_distances(self, starting_cell_row, starting_cell_column):
        """
        Set the distance grid to hold the distances from a starting cell
        """
        starting_cell = self.grid[starting_cell_row][starting_cell_column]
        # Calculate the distance from the stating cell to every other cell in grid
        self.distances = starting_cell.distances()

    def find_path_to(
        self,
        starting_cell_row,
        starting_cell_column,
        ending_cell_row,
        ending_row_column,
    ):
        """
        Set the distance grid to hold the distances representing the shortest path from a starting and ending cell
        """
        # Calc distances from a starting point
        self.calc_distances(starting_cell_row, starting_cell_column)
        # Calc shortest path from start to end then update distances member variable
        ending_cell = self.grid[ending_cell_row][ending_row_column]
        shortest_path = self.distances.path_to(ending_cell)
        self.distances = shortest_path

    def contents_of_cell(self, cell) -> str:
        """
        Helper function to pick what each cell should be displayed as in string representation.
        """
        if self.distances and self.distances.get_cell_distance(cell) is not None:
            # Use asterix to record spots in
            return "*"
        else:
            return " "

    def background_color_for(self, cell) -> tuple[int, int, int]:
        """
        If we've got distances then color the path each of them marks
        """
        if self.distances and self.distances.get_cell_distance(cell) is not None:
            return 200, 200, 200


class ColorGrid(Grid):
    """
    Given a grid and cell coordinates, colors all cells according to their distance from the starting cell
    """

    grid: List[List["Cell"]]
    cell: Cell
    distances: Distances
    max: int
    columns: int
    rows: int

    def __init__(self, grid, cell_row, cell_column):
        self.grid = grid.grid
        self.rows = grid.rows
        self.columns = grid.columns
        self.cell = grid.grid[cell_row][cell_column]
        self._distances(self.cell)

    def _distances(self, cell) -> None:
        """
        Calculate all the distances from the supplied cell
        """
        # Calculate all the distances from the target cell to everywhere else in the graph
        self.distances = cell.distances()
        _, self.max = self.distances.max()

    def background_color_for(self, cell) -> tuple[int, int, int]:
        """
        Color in each cell at a given intensity depending on how far it is from the supplied cell
        """
        distance = self.distances.get_cell_distance(cell)
        intensity = (self.max - distance) / self.max
        dark = 255 * intensity
        bright = 128 + (127 * intensity)
        return int(intensity), int(dark), int(bright)
