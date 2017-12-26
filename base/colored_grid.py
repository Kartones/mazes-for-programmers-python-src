from typing import cast, Optional, Tuple

from matplotlib.pyplot import get_cmap

from base.distance_grid import DistanceGrid
from base.cell import Cell

class ColoredGrid(DistanceGrid):

    def __init__(self, rows: int, columns: int, cmap:str='plasma') -> None:
        super().__init__(rows, columns)
        self.cmap = cmap

    @property
    def cmap(self):
        return self._cmap

    @cmap.setter
    def cmap(self, cmap):
        self._cmap = get_cmap(cmap)
    
    @cmap.getter
    def cmap(self):
        return self._cmap.name

    def background_color_for(self, cell: Cell) -> Optional[Tuple[int, int, int]]:
        if self.distances is not None and self.maximum > 0 and self.distances[cell] is not None:
            distance = self.distances[cell]
            if distance > 0 and distance < self.maximum:
                intensity = int((self.maximum - distance)/self.maximum*255)
                return tuple(int(x*255) for x in self._cmap(intensity))
            elif distance == self.maximum:
                return 128, 0, 0
            else:
                # starting cell in blue
                return 0, 148, 255
        else:
            return None
