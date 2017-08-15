
from base.grid import Grid
from base.cell import Cell


def test_constructor() -> None:
    grid = Grid(1, 1)
    assert grid.columns == 1
    assert grid.rows == 1

    grid = Grid(2, 2)
    assert grid.columns == 2
    assert grid.rows == 2


def test_cell_access() -> None:
    grid = Grid(2, 2)

    assert grid.get_cell(0, 0) == Cell(0, 0)    # type: ignore
    assert grid.get_cell(0, 1) == Cell(0, 1)    # type: ignore
    assert grid.get_cell(1, 0) == Cell(1, 0)    # type: ignore
    assert grid.get_cell(1, 1) == Cell(1, 1)    # type: ignore

    assert grid.get_cell(-1, 0) is None
    assert grid.get_cell(0, -1) is None
    assert grid.get_cell(4, 0) is None
    assert grid.get_cell(0, 4) is None


def test_neighbors_setup_when_grid_is_created() -> None:
    grid = Grid(2, 2)

    assert grid.get_cell(0, 0).north is None        # type: ignore
    assert grid.get_cell(0, 0).south == Cell(1, 0)  # type: ignore
    assert grid.get_cell(0, 0).east == Cell(0, 1)   # type: ignore
    assert grid.get_cell(0, 0).west is None         # type: ignore

    assert grid.get_cell(0, 1).north is None        # type: ignore
    assert grid.get_cell(0, 1).south == Cell(1, 1)  # type: ignore
    assert grid.get_cell(0, 1).east is None         # type: ignore
    assert grid.get_cell(0, 1).west == Cell(0, 0)   # type: ignore

    assert grid.get_cell(1, 0).north == Cell(0, 0)  # type: ignore
    assert grid.get_cell(1, 0).south is None        # type: ignore
    assert grid.get_cell(1, 0).east == Cell(1, 1)   # type: ignore
    assert grid.get_cell(1, 0).west is None         # type: ignore

    assert grid.get_cell(1, 1).north == Cell(0, 1)  # type: ignore
    assert grid.get_cell(1, 1).south is None        # type: ignore
    assert grid.get_cell(1, 1).east is None         # type: ignore
    assert grid.get_cell(1, 1).west == Cell(1, 0)   # type: ignore


def test_random_cell() -> None:
    grid = Grid(2, 2)

    for _ in range(100):
        assert grid.random_cell() in [Cell(0, 0), Cell(0, 1), Cell(1, 0), Cell(1, 1)]


def test_size() -> None:
    assert Grid(1, 1).size() == 1
    assert Grid(2, 2).size() == 4
    assert Grid(3, 3).size() == 9
