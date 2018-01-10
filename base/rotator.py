from typing import TYPE_CHECKING, Tuple

from base.grid import Grid
from base.cell import Cell

if TYPE_CHECKING:
    from base.distance_grid import DistanceGrid  # noqa: F401
    from base.colored_grid import ColoredGrid  # noqa: F401
else:
    DistanceGrid = 'DistanceGrid'
    ColoredGrid = 'ColoredGrid'

Point = Tuple[int, int]


class Rotator:
    '''
    Each rotation is always 90 degrees clockwise.
    Not present in the book but suggested as exercise. Good for mitigating weak algorithm straight paths.
    '''

    def on(self, grid: Grid) -> Grid:
        grid_type = type(grid)

        # row i becomes col n-i when rotating 90 degrees clockwise
        rotated_grid = grid_type(rows=grid.cols, cols=grid.rows)

        for old_cell in grid.eachCell():
            row, column = self._rotated_coordinates(old_cell, rotated_grid)
            new_cell = rotated_grid[row, column]
            if new_cell is None:
                raise IndexError('Cell not found at row {} column {}'.format(row, column))
            self._rotate_cell_neighbors(new_cell, old_cell, rotated_grid)

        return rotated_grid

    @staticmethod
    def _rotated_coordinates(cell: Cell, grid: Grid) -> Point:
        row = cell.col
        column = (grid.cols - cell.row - 1)
        return row, column

    def _rotate_cell_neighbors(self, new: Cell, old: Cell, grid: Grid) -> None:
        for link in old.links:
            row, col = self._rotated_coordinates(link, grid)
            neighbor = grid[row, col]
            if neighbor is None:
                raise IndexError('Cell not found at row {} column {}'.format(row, col))
            new.link(neighbor)
