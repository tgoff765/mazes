from random import randint
from typing import Union


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
        x = randint(0, self.rows - 1)
        y = randint(0, self.columns - 1)
        while not (self.bits[y][x]):
            x = randint(0, self.rows - 1)
            y = randint(0, self.columns - 1)

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
