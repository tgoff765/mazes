from maze_creator.core.cells import Cell


def test_no_neighbors():
    """
    Unlinked cells should have a links length of 0
    """
    test_cell = Cell(1, 1)
    assert len(test_cell.links()) == 0


def test_link():
    test_cell = Cell(1,1)
    test_cell_2 = Cell(2,2)
    test_cell.link(test_cell_2)
    assert test_cell.is_linked(test_cell_2)
