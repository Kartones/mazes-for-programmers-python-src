from typing import Tuple

from base.distance_grid import DistanceGrid


Point = Tuple[int, int, int]


def calculate(grid: DistanceGrid) -> Tuple[Point, Point, Point]:
    """
    Calculates a longest path inside a maze, by calculating the longest past from nortwest corner,
    then using that point as the actual start and calculating its most distant cell.
    """
    start_cell = grid[0, 0, 0]
    if start_cell is None:
        raise IndexError("Invalid start cell row {} column {}".format(0, 0))

    new_start_cell, distance = start_cell.distances.max
    goal_cell, distance = new_start_cell.distances.max

    return (new_start_cell.level, new_start_cell.row, new_start_cell.column), (goal_cell.level, goal_cell.row, goal_cell.column)
