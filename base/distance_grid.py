from typing import Optional, Any

from base.grid import Grid
from base.cell import Cell
from base.distances import Distances

'''
Distance is represented as hexadecimal
'''


class DistanceGrid(Grid):

    @property
    def distances(self) -> Optional[Distances]:
        return None if self._distances is None else self._distances  # mypy messes up with Any and Optional :(

    @distances.setter
    def distances(self, value: Optional[Distances]) -> None:
        self._distances = value
        if self._distances is not None:
            _, self.maximum = self._distances.max

    def __init__(self, rows: int, columns: int) -> None:
        super().__init__(rows, columns)
        self._distances = None  # type: Optional[Distances]
        self.maximum = 0  # type: int

    def contents(self, cell: Cell) -> str:
        if self.distances is not None and self.distances[cell]:
            return format(self.distances[cell], '02X').center(3)
        else:
            return super().contents(cell)


def isDistanceGrid(grid: Any) -> bool:
    ''' Runtime class check '''
    return isinstance(grid, DistanceGrid)
