from typing import Optional, Tuple

from base.distance_grid import DistanceGrid
from base.cell import Cell
from base.distances import Distances    # noqa: F401


class ColoredGrid(DistanceGrid):

    # Need to redefine getter to redefine setter
    @property
    def distances(self) -> Optional[Distances]:
        return None if self._distances is None else self._distances     # mypy messes up with Any and Optional :(

    @distances.setter
    def distances(self, value: Optional[Distances]) -> None:
        self._distances = value
        if self._distances is not None:
            _, self.maximum = self._distances.max

    def background_color_for(self, cell: Cell) -> Optional[Tuple[int, int, int]]:
        if self.distances is not None and self.maximum is not None and self.distances[cell]:
            distance = self.distances[cell]
            intensity = float((self.maximum - distance)) / self.maximum   # type: ignore
            dark = round(255 * intensity)
            bright = 128 + round(127 * intensity)
            return dark, bright, dark
        else:
            return None
