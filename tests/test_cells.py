from maze_creator.core.cells import Cell


def test_no_neighbors():
    """
    Unlinked cells should have a links length of 0
    """
    test_cell = Cell(1, 1)
    assert len(test_cell.links()) == 0
