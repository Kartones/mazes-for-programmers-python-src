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


def test_max_distance() -> None:
    cell_1 = Cell(0, 0)
    distances = Distances(cell_1)

    cell_2 = Cell(0, 1)
    distance_from_2_to_1 = 4
    distances[cell_2] = distance_from_2_to_1

    cell_3 = Cell(1, 0)
    distance_from_3_to_1 = 5
    distances[cell_3] = distance_from_3_to_1

    cell_4 = Cell(2, 0)
    distance_from_4_to_1 = 8
    distances[cell_4] = distance_from_4_to_1

    assert distances.max == (cell_4, distance_from_4_to_1,)
