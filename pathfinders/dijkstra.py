from base.distance_grid import DistanceGrid


def calculate_distances(grid: DistanceGrid, start_row: int, start_column: int, end_row: int,
                        end_column: int) -> DistanceGrid:
    start_cell = grid.get_cell(start_row, start_column)
    if start_cell is None:
        raise IndexError("Invalid start cell row {} column {}".format(start_row, start_column))
    destination_cell = grid.get_cell(end_row, end_column)
    if destination_cell is None:
        raise IndexError("Invalid destination cell row {} column {}".format(end_row, end_row))
    distances = start_cell.distances()
    grid.distances = distances.path_to(destination_cell)

    return grid
