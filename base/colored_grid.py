from typing import cast, Optional, Tuple

from base.distance_grid import DistanceGrid
from base.cell import Cell

MAX_DARK = 210                          # Dark meaning farther than or more distant than
MAX_BRIGHT = round(MAX_DARK / 2)        # And thus, bright means closer than or less distant than
MAX_BRIGHT_INTENSITY = MAX_BRIGHT - 1


class ColoredGrid(DistanceGrid):

    def background_color_for(self, cell: Cell) -> Optional[Tuple[int, int, int]]:
        if self.distances is not None and self.maximum > 0 and self.distances[cell] is not None:
            distance = cast(int, self.distances[cell])
            if distance > 0 and distance < self.maximum:
                intensity = float((self.maximum - distance)) / self.maximum
                dark = round(MAX_DARK * intensity)
                bright = MAX_BRIGHT + round(MAX_BRIGHT_INTENSITY * intensity)
                return dark, bright, dark
            elif distance == self.maximum:
                return 128, 0, 0
            else:
                # starting cell in blue
                return 0, 148, 255
        else:
            return None
