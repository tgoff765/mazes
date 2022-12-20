from maze_creator.core.cells import Cell


def test_no_neighbors():
    test_cell = Cell(1, 1)
    assert len(test_cell.links()) == 0


def test_multiple_neighbors():
    test_cell = Cell(1, 1)
    test_cell_2 = Cell(1, 2)
    test_cell_3 = Cell(2, 1)
    test_cell.link(test_cell_2)
    test_cell.link(test_cell_3)
    assert len(test_cell.links()) == 2


def test_link():
    test_cell = Cell(1, 1)
    test_cell_2 = Cell(2, 2)
    test_cell.link(test_cell_2)
    assert test_cell.is_linked(test_cell_2)


def test_unlink():
    test_cell = Cell(1, 1)
    test_cell_2 = Cell(2, 2)
    test_cell.link(test_cell_2)
    test_cell.unlink(test_cell_2)
    assert not test_cell.is_linked(test_cell_2)
