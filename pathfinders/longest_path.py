from typing import Tuple

from base.distance_grid import DistanceGrid

'''
Calculates a longest path inside a maze, by calculating the longest past from nortwest corner, then using that point as
the actual start and calculating its most distant cell.
'''

Point = Tuple[int, int]


def calculate(grid: DistanceGrid) -> Tuple[Point, Point]:
    start_cell = grid[0, 0]
    if start_cell is None:
        raise IndexError('Invalid start cell row {} column {}'.format(0, 0))

    new_start_cell, distance = start_cell.distances.max
    goal_cell, distance = new_start_cell.distances.max

    start = (new_start_cell.row, new_start_cell.col)
    end = (goal_cell.row, goal_cell.col)

    return start, end
