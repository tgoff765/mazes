from random import randint
from typing import Union
import os
from PIL import Image


class Mask:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.bits = [[True for _ in range(columns)] for _ in range(rows)]

    def count(self):
        """
        How many locations are enabled in the mask
        """
        count = 0
        for rows in self.bits:
            for bool in rows:
                if bool:
                    count += 1

        return count

    def random_location(self):
        """
        Pick a random location from the gird that's enabled
        """
        x = randint(0, self.columns - 1)
        y = randint(0, self.rows - 1)
        while not (self.bits[y][x]):
            x = randint(0, self.columns - 1)
            y = randint(0, self.rows - 1)

        return (y, x)

    def __getitem__(self, tup) -> Union["Cell", None]:
        """
        Return a slice of the underlying grid only if the rows and columns are non-negative, otherwise return None
        This way we can access the Cell of a Grid by Grid[row, column]
        """
        y, x = tup
        if 0 <= y <= (self.rows - 1) and 0 <= x <= (self.columns - 1):
            return self.bits[y][x]
        return None

    @staticmethod
    def from_txt(file):
        path = os.path.abspath(file)
        f = open(path, "r")
        lines = f.readlines()
        f.close()

        cleaned_lines = [l.strip() for l in lines]
        rows = len(cleaned_lines)
        columns = len(cleaned_lines[0])
        mask = Mask(rows, columns)

        cur_row = 0
        cur_col = 0
        while cur_row < rows:
            while cur_col < columns:
                if cleaned_lines[cur_row][cur_col] == "X":
                    mask.bits[cur_row][cur_col] = False
                cur_col += 1

            cur_col = 0
            cur_row += 1

        return mask

    @staticmethod
    def from_image(image):
        path = os.path.abspath(image)
        img = Image.open(path)
        mask = Mask(img.height, img.width)
        cur_row = 0
        cur_col = 0
        while cur_row < img.height:
            while cur_col < img.width:
                pixel_color = img.getpixel((cur_col,cur_row))
                if pixel_color == (0,0,0):
                     mask.bits[cur_row][cur_col] = False
                cur_col += 1

            cur_col = 0
            cur_row += 1

        return mask


if __name__ == "__main__":
    mask = Mask.from_image("../../docs/masks/olaf.png")
    print(mask)
