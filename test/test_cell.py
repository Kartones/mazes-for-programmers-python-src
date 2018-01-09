
from base.cell import Cell


def test_equality() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 1)
    assert a_cell != another_cell


def test_linking() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)

    assert not a_cell & another_cell
    assert not another_cell & a_cell
    assert not a_cell & yet_another_cell
    assert not another_cell & yet_another_cell

    a_cell += another_cell

    assert a_cell & another_cell
    assert another_cell & a_cell
    assert not a_cell & yet_another_cell
    assert not another_cell & yet_another_cell


def test_unlinking() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)

    a_cell += another_cell
    a_cell += yet_another_cell

    assert a_cell & another_cell
    assert another_cell & a_cell
    assert a_cell & yet_another_cell

    a_cell -= another_cell

    assert not a_cell & another_cell
    assert not another_cell & a_cell
    assert a_cell & yet_another_cell
    assert yet_another_cell & a_cell


def test_links_listing() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)

    a_cell += another_cell
    a_cell += yet_another_cell

    assert set(a_cell.links).intersection([another_cell, yet_another_cell]) == set(a_cell.links)
    assert another_cell.links == [a_cell]
    assert yet_another_cell.links == [a_cell]


def test_has_no_neighbors() -> None:
    assert Cell(1, 1).neighbours == []


def test_has_neighbors() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)

    a_cell.north = another_cell
    another_cell.south = yet_another_cell
    yet_another_cell.east = another_cell
    yet_another_cell.west = a_cell

    assert another_cell in a_cell.neighbours
    assert yet_another_cell not in a_cell.neighbours
    assert a_cell.nNeighbours == 1
    assert a_cell not in another_cell.neighbours
    assert yet_another_cell in another_cell.neighbours
    assert another_cell.nNeighbours == 1
    assert a_cell in yet_another_cell.neighbours
    assert another_cell in yet_another_cell.neighbours
    assert yet_another_cell.nNeighbours == 2


def test_distances() -> None:
    a_cell = Cell(0, 0)
    another_cell = Cell(0, 1)
    yet_another_cell = Cell(0, 2)

    a_cell.east = another_cell
    a_cell += another_cell
    another_cell.east = yet_another_cell
    another_cell += yet_another_cell
    distances = a_cell.distances
    assert set(distances.cells) == {yet_another_cell, another_cell, a_cell}
    assert distances[a_cell] == 0
    assert distances[another_cell] == 1
    assert distances[yet_another_cell] == 2
