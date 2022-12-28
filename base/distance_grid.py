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
        self._distances: Optional[Distances] = None
        self.maximum: int = 0

    @property
    def distances(self) -> Optional[Distances]:
        return self._distances

    @distances.setter
    def distances(self, value: Optional[Distances]) -> None:
        self._distances = value
        if self._distances:
            _, self.maximum = self._distances.max

    def contents_of(self, cell: Cell) -> str:
        if self.distances is not None and self.distances[cell] is not None:
            return format(self.distances[cell], "02X").center(3)
        else:
            return super().contents_of(cell)
