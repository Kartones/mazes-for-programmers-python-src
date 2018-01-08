from typing import Tuple

from base.distance_grid import DistanceGrid

Point = Tuple[int, int]


def calculate_distances(grid: DistanceGrid, start: Point, end: Point) -> None:
    ''' Calculate the distances in the grid using Dijkstra's algorithm '''

    start_cell = grid[start]
    if start_cell is None:
        raise IndexError('Invalid start cell row {} column {}'.format(*start))

    end_cell = grid[end]
    if end_cell is None:
        raise IndexError('Invalid destination cell row {} column {}'.format(*end))

    grid.distances = start_cell.distances.pathTo(end_cell)
