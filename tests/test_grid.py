from maze_creator.core.grid import Grid


def test_grid_setup():
    test_grid = Grid(2, 2)
    assert test_grid.columns == 2
    assert test_grid.rows == 2


def test_grid_size():
    test_grid = Grid(2, 5)
    assert test_grid.size() == 10
