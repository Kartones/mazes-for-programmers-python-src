from typing import Optional     # noqa: F401

from base.grid import Grid
from base.cell import Cell
from base.distances import Distances    # noqa: F401

"""
Distance is represented as hexadecimal
"""


class DistanceGrid(Grid):

    def __init__(self, rows: int, columns: int) -> None:
        super().__init__(rows, columns)
        self.distances = None  # type: Optional[Distances]

    def contents_of(self, cell: Cell) -> str:
        if self.distances is not None and self.distances[cell]:
            return format(self.distances[cell], "X").center(3)
        else:
            return super().contents_of(cell)
