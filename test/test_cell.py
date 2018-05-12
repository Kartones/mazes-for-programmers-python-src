
from base.cell import Cell


def test_equality() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 1)
    assert a_cell == another_cell


def test_linking() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)

    assert a_cell.linked_to(another_cell) is False
    assert another_cell.linked_to(a_cell) is False
    assert a_cell.linked_to(yet_another_cell) is False
    assert another_cell.linked_to(yet_another_cell) is False

    a_cell.link(another_cell)

    assert a_cell.linked_to(another_cell) is True
    assert another_cell.linked_to(a_cell) is True
    assert a_cell.linked_to(yet_another_cell) is False
    assert another_cell.linked_to(yet_another_cell) is False


def test_linking_using_operator_overloads() -> None:
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

    a_cell.link(another_cell)
    a_cell.link(yet_another_cell)

    assert a_cell.linked_to(another_cell) is True
    assert another_cell.linked_to(a_cell) is True
    assert a_cell.linked_to(yet_another_cell) is True

    a_cell.unlink(another_cell)

    assert a_cell.linked_to(another_cell) is False
    assert another_cell.linked_to(a_cell) is False
    assert a_cell.linked_to(yet_another_cell) is True
    assert yet_another_cell.linked_to(a_cell) is True


def test_unlinking_using_operator_overrides() -> None:
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
    assert Cell(1, 1).neighbors == []


def test_has_neighbors() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)

    a_cell.north = another_cell
    another_cell.south = yet_another_cell
    yet_another_cell.east = another_cell
    yet_another_cell.west = a_cell

    assert another_cell in a_cell.neighbors
    assert yet_another_cell not in a_cell.neighbors
    assert len(a_cell.neighbors) == 1
    assert a_cell not in another_cell.neighbors
    assert yet_another_cell in another_cell.neighbors
    assert len(another_cell.neighbors) == 1
    assert a_cell in yet_another_cell.neighbors
    assert another_cell in yet_another_cell.neighbors
    assert len(yet_another_cell.neighbors) == 2


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
