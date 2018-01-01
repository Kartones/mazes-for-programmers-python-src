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

    def color(self, cell: Cell) -> Optional[Tuple[int, int, int]]:
        if self.distances is not None and self.maximum > 0 and self.distances[cell] is not None:
            distance = self.distances[cell]
            intensity = int((self.maximum - distance)/self.maximum*255)
            color = tuple(int(x*255) for x in self._cmap(intensity))
            color = color[:3] # Use RGB only
            # Invert the starting and the ending points
            if distance == self.maximum or distance == 0:
                color = tuple(int(255-x) for x in color) # Invert
                color = tuple(color[xi-2] for xi in range(len(color))) # Rotate channels
            return color
        else:
            return 255, 255, 255
