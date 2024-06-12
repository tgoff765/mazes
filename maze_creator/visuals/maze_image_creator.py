from PIL import Image, ImageDraw, ImageOps


class ColorChoice:
    BLUE = 1
    DARKGREEN = 2
    PURPLE = 3
    GREEN = 4
    RED = 5
    YELLOW = 6


# TODO: Need to figure out a class hierarchy that can deal with this
class MazeImageCreator:
    """
    Given some grid, create a nice image of it
    """

    def __init__(self, maze, type="bw", color_choice: ColorChoice = ColorChoice.BLUE):
        self.maze = maze
        self.grid = maze.grid
        self.type = type
        self.color_choice = color_choice

    def background_color_for(self, cell, canvas_color, color_choice):
        """
        Pick what the background color for each cell should be in the image
        """
        if cell is None:
            return canvas_color
        if self.type == "bw":
            return None
        elif self.type == "path":
            if self.maze.path and self.maze.path.get_cell_distance(cell) is not None:
                return 200, 200, 200
        elif self.type == "distance":
            distance = self.maze.distances.get_cell_distance(cell)
            intensity = (self.maze.max - distance) / self.maze.max
            dark = 255 * intensity
            bright = 128 + (127 * intensity)
            # We can vary these
            if color_choice == ColorChoice.BLUE:
                return int(intensity), int(dark), int(bright)
            elif color_choice == ColorChoice.DARKGREEN:
                return int(intensity), int(bright), int(dark)
            elif color_choice == ColorChoice.PURPLE:
                return int(dark), int(intensity), int(bright)
            elif color_choice == ColorChoice.GREEN:
                return int(dark), int(bright), int(intensity)
            elif color_choice == ColorChoice.RED:
                return int(bright), int(intensity), int(dark)
            elif color_choice == ColorChoice.YELLOW:
                return int(bright), int(dark), int(intensity)
        # Color by number of openings
        elif self.type == "openings":
            num_of_neighbors = len(cell.links())
            openings_color_map = {
                4: (0, 204, 0),
                3: (51, 255, 51),
                2: (153, 255, 153),
                1: (255, 255, 255),
            }
            return openings_color_map.get(num_of_neighbors, 1)

    def draw(
        self,
        cell_size: int = 100,
        canvas_color: (int, int, int) = (255, 255, 255),
        line_color: (int, int, int) = (0, 0, 0),
        line_thickness: int = 10,
    ) -> Image:
        """
        Draw grid to canvas using the Pillow Library
        Note that a weakness of this rendering is that line width is drawn inside cells (instead of as a separate grid)
        which means that if line_width is large enough it'll draw over the cell.
        In a future edit will need to disentangle the gridlines and the cells.
        In general, I'd recommend keeping line_thickness 10% the size of cell_size or less.
        """

        img_width = cell_size * self.grid.columns
        img_height = cell_size * self.grid.rows
        im = Image.new("RGB", (img_width + 1, img_height + 1), canvas_color)

        # Create a drawable version of the image
        draw = ImageDraw.Draw(im)

        # Draw each of the cells onto the image
        current_row = 0
        for row in self.grid.each_row():
            # Iterate through each mode, one iteration to loop through backgrounds, another to do cell walls
            for mode in ["backgrounds", "walls"]:
                current_column = 0
                for cell in row:
                    if cell is None:
                        x1 = current_column * cell_size
                        y1 = current_row * cell_size
                        x2 = (current_column + 1) * cell_size
                        y2 = (current_row + 1) * cell_size
                    else:
                        # Calc the northwest and southeast corner points, accounting for
                        x1 = cell.column * cell_size
                        y1 = cell.row * cell_size
                        x2 = (cell.column + 1) * cell_size
                        y2 = (cell.row + 1) * cell_size

                    if mode == "backgrounds":
                        color = self.background_color_for(
                            cell, canvas_color, self.color_choice
                        )
                        if color and cell is not None:

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
                        # Hack for masked cells
                        if cell is None:
                            if current_row == 0:
                                draw.line(
                                    ((x1, y1), (x2, y1)), line_color, line_thickness
                                )

                            if current_column == 0:
                                draw.line(
                                    ((x1, y1), (x1, y2)), line_color, line_thickness
                                )

                            draw.line(((x1, y2), (x2, y2)), line_color, line_thickness)

                            draw.line(((x2, y1), (x2, y2)), line_color, line_thickness)

                        else:
                            # Since every cell draws its southern and eastern borders, we only have to
                            # draw northern and western borders if the cell has no neighbor in that direction
                            if not cell.north:
                                draw.line(
                                    ((x1, y1), (x2, y1)), line_color, line_thickness
                                )

                            if not cell.west:
                                draw.line(
                                    ((x1, y1), (x1, y2)), line_color, line_thickness
                                )

                            # Every cell draws its own southern and eastern borders unless it is linked to that neighbor
                            if not cell.is_linked(cell.south):
                                draw.line(
                                    ((x1, y2), (x2, y2)), line_color, line_thickness
                                )

                            if not cell.is_linked(cell.east):
                                draw.line(
                                    ((x2, y1), (x2, y2)), line_color, line_thickness
                                )

                    current_column += 1

            current_row += 1

        img_with_border = ImageOps.expand(im, border=10, fill="black")
        return img_with_border.show()
