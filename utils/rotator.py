from typing import Tuple, Union

from base.grid import Grid
from base.distance_grid import DistanceGrid
from base.cell import Cell


class Rotator:
    """
    Each rotation is always 90 degrees clockwise.
    Not present in the book but suggested as exercise. Good for mitigating weak algorithm straight paths.
    """

    @staticmethod
    def on(grid: Union[Grid, DistanceGrid]) -> Union[Grid, DistanceGrid]:
        # row i becomes col n-i when rotating 90 degrees clockwise
        rotated_grid = Grid(rows=grid.columns, columns=grid.rows)

        for old_cell in grid.each_cell():
            row, column = Rotator._rotated_coordinates(old_cell, rotated_grid)
            new_cell = rotated_grid.get_cell(row, column)
            if new_cell is None:
                raise IndexError("Cell not found at row {} column {}".format(row, column))
            Rotator._rotate_cell_neighbors(new_cell, old_cell, rotated_grid)

        return rotated_grid

    @staticmethod
    def _rotated_coordinates(cell: Cell, grid: Grid) -> Tuple[int, int]:
        row = cell.column
        column = (grid.columns - cell.row - 1)
        return row, column

    @staticmethod
    def _rotate_cell_neighbors(new_cell: Cell, old_cell: Cell, grid: Grid) -> None:
        for link in old_cell.links:
            row, column = Rotator._rotated_coordinates(link, grid)
            neighbor = grid.get_cell(row, column)
            if neighbor is None:
                raise IndexError("Cell not found at row {} column {}".format(row, column))
            new_cell.link(neighbor)
