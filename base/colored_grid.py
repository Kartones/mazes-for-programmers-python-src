from typing import Optional, Tuple, Union, cast

from matplotlib.colors import Colormap
from matplotlib.pyplot import get_cmap

from base.cell import Cell
from base.distance_grid import DistanceGrid

RGBColor = Tuple[int, int, int]


class ColoredGrid(DistanceGrid):

    def __init__(self, rows: int, columns: int, cmap: str = 'plasma') -> None:
        super().__init__(rows, columns)
        self.cmap = cmap

    @property
    def cmap(self) -> Colormap:
        return self._cmap

    @cmap.setter
    def cmap(self, cmap: Union[str, Colormap]) -> None:
        self._cmap = get_cmap(cmap)

    @cmap.getter
    def cmap(self) -> str:
        return str(self._cmap.name)

    def _getColor(self, value: int) -> RGBColor:
        color = self._cmap(value)
        if not self._isValidColor(color): return (255, 255, 255)  # Return white if colormap returns an invalid color
        return cast(RGBColor, tuple(int(x * 255) for x in color))  # Convert to [0, 255] range

    @staticmethod
    def _isValidColor(color: RGBColor) -> bool:
        ''' Runtime check for color correctness '''
        return type(color) == tuple and len(color) == 3 and not any(type(x) != int for x in color)

    def color(self, cell: Cell) -> Optional[Tuple[int, int, int]]:
        if self.distances is not None and self.maximum > 0 and self.distances[cell] is not None:
            distance = cast(int, self.distances[cell])
            intensity = int((self.maximum - distance) / self.maximum * 255)
            color = self._getColor(intensity)
            # Invert the starting and the ending points
            if distance == self.maximum or distance == 0:
                color = cast(RGBColor, tuple(int(255 - x) for x in color))  # Invert
                color = cast(RGBColor, tuple(color[xi - 2] for xi in range(3)))  # Rotate channels
            return color
        else:
            return 255, 255, 255
