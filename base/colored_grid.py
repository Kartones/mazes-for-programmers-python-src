from typing import Optional, Tuple

from base.distance_grid import DistanceGrid
from base.cell import Cell
from base.distances import Distances    # noqa: F401

MAX_DARK = 210                          # Dark meaning farther than or more distant than
MAX_BRIGHT = round(MAX_DARK / 2)        # And thus, bright means closer than or less distant than
MAX_BRIGHT_INTENSITY = MAX_BRIGHT - 1


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
        if self.distances is not None and self.maximum is not None and self.distances[cell] is not None:
            distance = self.distances[cell]
            if distance > 0:
                intensity = float((self.maximum - distance)) / self.maximum   # type: ignore
                dark = round(MAX_DARK * intensity)
                bright = MAX_BRIGHT + round(MAX_BRIGHT_INTENSITY * intensity)
                return dark, bright, dark
            else:
                # starting cell in blue
                return 0, 148, 255
        else:
            return None
