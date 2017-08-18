from base.distance_grid import DistanceGrid

"""
Note: Assumes grid has already been applied a maze algorithm
"""


def calculate_distances(grid: DistanceGrid, start_row: int, start_column: int) -> DistanceGrid:
    start = grid.get_cell(start_row, start_column)
    if start is None:
        raise IndexError("Invalid start cell row {} column {}".format(start_row, start_column))
    distances = start.distances()
    grid.distances = distances
    return grid
