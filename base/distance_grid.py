from typing import Optional     # noqa: F401

from base.grid import Grid
from base.cell import Cell
from base.distances import Distances    # noqa: F401

"""
Distance is represented as hexadecimal
"""


class DistanceGrid(Grid):

    @property
    def distances(self) -> Optional[Distances]:
        return None if self._distances is None else self._distances     # mypy messes up with Any and Optional :(

    @distances.setter
    def distances(self, value: Optional[Distances]) -> None:
        self._distances = value

    def __init__(self, rows: int, columns: int) -> None:
        super().__init__(rows, columns)
        self._distances = None  # type: Optional[Distances]

    def contents_of(self, cell: Cell) -> str:
        if self.distances is not None and self.distances[cell]:
            return format(self.distances[cell], "X").center(3)
        else:
            return super().contents_of(cell)
