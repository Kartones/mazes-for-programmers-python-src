from typing import Tuple

from base.distance_grid import DistanceGrid


Point = Tuple[int, int]


def calculate_distances(grid: DistanceGrid, start: Point, end: Point) -> None:
    """
    Calculate the distances in the grid using Dijkstra's algorithm
    """
    if grid[start] is None:
        raise IndexError("Invalid start cell {} column {}".format(*start))
    if grid[end] is None:
        raise IndexError("Invalid destination cell row {} column {}".format(*end))

    grid.distances = grid[start].distances.path_to(grid[end])  # type: ignore
