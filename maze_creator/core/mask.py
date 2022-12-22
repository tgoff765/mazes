from random import randint
from typing import List, Union


class Mask:
    """
    Mask stores the cells in our maze that we want to toggle on/off using the bits array
    """

    rows: int
    columns: int
    bits = List[List[bool]]

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.bits = [[True for column in range(columns)] for row in range(rows)]

    def __getitem__(self, tup) -> Union[bool, None]:
        """
        Return a slice of the underlying grid only if the rows and columns are non-negative, otherwise return None
        This way we can access the bits of a Mask by Mask[row, column]
        """
        y, x = tup
        if 0 <= y <= (self.rows - 1) and 0 <= x <= (self.columns - 1):
            return self.bits[y][x]
        return None

    def __setitem__(self, tup, value) -> None:
        """
        Similar to getitem, allows us to set the value of a mask using Mask[row, column] = T/F notation
        """
        y, x = tup
        if 0 <= y <= (self.rows - 1) and 0 <= x <= (self.columns - 1):
            self.bits[y][x] = value
        else:
            raise Exception("Tuple index value out of range")

    def count(self) -> int:
        """
        Return the number of cells in our mask that are turned on
        """
        num_bits_turned_on = 0
        for row in self.bits:
            for bit in row:
                if bit:
                    num_bits_turned_on += 1

        return num_bits_turned_on

    def random_location(self) -> tuple[int, int]:
        """
        Return a random enabled location
        """
        # Keep picking a random set of locations until we get one that is enabled
        rand_row = randint(0, self.rows - 1)
        rand_column = randint(0, self.columns - 1)

        while self.bits[rand_row][rand_column] is not True:
            rand_row = randint(0, self.rows - 1)
            rand_column = randint(0, self.columns - 1)

        return rand_row, rand_column


if __name__ == "__main__":
    test = Mask(3, 3)
    print(test.random_location())
