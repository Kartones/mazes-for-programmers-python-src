from typing import Union

from base.distance_grid import DistanceGrid
from base.colored_grid import ColoredGrid


def calculate_distances(grid: Union[DistanceGrid, ColoredGrid], start_row: int, start_column: int, end_row: int,
                        end_column: int) -> Union[DistanceGrid, ColoredGrid]:
    start_cell = grid.cell_at(start_row, start_column)
    if start_cell is None:
        raise IndexError("Invalid start cell row {} column {}".format(start_row, start_column))
    destination_cell = grid.cell_at(end_row, end_column)
    if destination_cell is None:
        raise IndexError("Invalid destination cell row {} column {}".format(end_row, end_row))
    distances = start_cell.distances
    grid.distances = distances.path_to(destination_cell)

    return grid
