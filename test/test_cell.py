
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


def test_links_listing() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)

    a_cell.link(another_cell)
    a_cell.link(yet_another_cell)

    assert set(a_cell.links).intersection([another_cell, yet_another_cell]) == set(a_cell.links)
    assert another_cell.links == [a_cell]
    assert yet_another_cell.links == [a_cell]


def test_has_no_neighbors() -> None:
    assert Cell(1, 1).neighbors() == []


def test_has_neighbors() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)

    a_cell.north = another_cell
    another_cell.south = yet_another_cell
    yet_another_cell.east = another_cell
    yet_another_cell.west = a_cell

    assert another_cell in a_cell.neighbors()
    assert yet_another_cell not in a_cell.neighbors()
    assert len(a_cell.neighbors()) == 1
    assert a_cell not in another_cell.neighbors()
    assert yet_another_cell in another_cell.neighbors()
    assert len(another_cell.neighbors()) == 1
    assert a_cell in yet_another_cell.neighbors()
    assert another_cell in yet_another_cell.neighbors()
    assert len(yet_another_cell.neighbors()) == 2
