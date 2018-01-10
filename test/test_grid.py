
from base.grid import Grid
from base.cell import Cell


def test_constructor() -> None:
    grid = Grid(2, 2)
    assert grid.cols == 2
    assert grid.rows == 2

    grid = Grid(3, 3)
    assert grid.cols == 3
    assert grid.rows == 3


def test_cell_access() -> None:
    grid = Grid(2, 2)

    assert grid[0, 0] == Cell(0, 0)
    assert grid[0, 1] == Cell(0, 1)
    assert grid[1, 0] == Cell(1, 0)
    assert grid[1, 1] == Cell(1, 1)

    assert grid[-1,  0] is None
    assert grid[ 0, -1] is None  # noqa: E201
    assert grid[ 4,  0] is None  # noqa: E201
    assert grid[ 0,  4] is None  # noqa: E201


def test_neighbors_setup_when_grid_is_created() -> None:
    grid = Grid(2, 2)

    assert grid[0, 0].north is None        # type: ignore
    assert grid[0, 0].south == Cell(1, 0)  # type: ignore
    assert grid[0, 0].east == Cell(0, 1)   # type: ignore
    assert grid[0, 0].west is None         # type: ignore

    assert grid[0, 1].north is None        # type: ignore
    assert grid[0, 1].south == Cell(1, 1)  # type: ignore
    assert grid[0, 1].east is None         # type: ignore
    assert grid[0, 1].west == Cell(0, 0)   # type: ignore

    assert grid[1, 0].north == Cell(0, 0)  # type: ignore
    assert grid[1, 0].south is None        # type: ignore
    assert grid[1, 0].east == Cell(1, 1)   # type: ignore
    assert grid[1, 0].west is None         # type: ignore

    # TODO: None Cell class
    assert grid[1, 1].north == Cell(0, 1)  # type: ignore
    assert grid[1, 1].south is None        # type: ignore
    assert grid[1, 1].east is None         # type: ignore
    assert grid[1, 1].west == Cell(1, 0)   # type: ignore


def test_random_cell() -> None:
    grid = Grid(2, 2)

    for _ in range(100):
        assert grid.randomCell() in [Cell(0, 0), Cell(0, 1), Cell(1, 0), Cell(1, 1)]


def test_size() -> None:
    assert Grid(2, 2).size == 4
    assert Grid(3, 3).size == 9
    assert Grid(4, 4).size == 16
