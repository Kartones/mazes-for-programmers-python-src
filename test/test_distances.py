from base.distances import Distances
from base.cell import Cell


def test_index_access() -> None:
    a_cell = Cell(0, 0)
    distances = Distances(a_cell)

    assert distances[a_cell] == 0

    another_cell = Cell(0, 1)
    distance = 13
    distances[another_cell] = distance
    assert distances[another_cell] == distance

    assert distances[Cell(2, 2)] is None
