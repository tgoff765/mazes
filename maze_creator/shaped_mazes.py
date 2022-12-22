from maze_creator.algos.aldousbroder import AldousBroder
from maze_creator.core.grid import MaskedGrid
from maze_creator.core.mask import Mask

if __name__ == "__main__":
    test_mask = Mask(5, 5)
    test_mask[1, 1] = False
    test_mask[4, 4] = False
    test_mask_grid = MaskedGrid(test_mask)
    test_maze = AldousBroder(rows=5, columns=5)
    test_maze.grid = test_mask_grid
    test_maze.create_maze()
    print(test_maze)
