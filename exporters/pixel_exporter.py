from time import gmtime, strftime
from typing import TYPE_CHECKING, Any, Union

import numpy as np
from PIL import Image, ImageDraw

from base.colored_grid import ColoredGrid
from exporters.base_exporter import BaseExporter

if TYPE_CHECKING:
    from base.grid import Grid  # noqa: F401


class PixelExporter(BaseExporter):
    ''' Export grid into a pixel-perfect image '''

    def render(self, grid: Union["Grid", ColoredGrid], **kwargs: Any) -> None:
        ''' Main render method '''
        assert isinstance(grid, ColoredGrid)
        f, cs, clr = self._processKwargs(**kwargs)
        image = self._render(grid, cs, clr)
        image.save("{}.png".format(f), "PNG", optimize=True)

    @staticmethod
    def _render(grid, cs=4, clr=False) -> Image:
        ''' Rendering core '''
        arr = np.zeros((cs*grid.rows+2, cs*grid.columns+2, 3))
        # Outermost walls
        arr[ :, 0,0:3] = 0
        arr[ :,-1,0:3] = 0
        arr[ 0, :,0:3] = 0
        arr[-1, :,0:3] = 0
        # Draw each cell
        for ri, row in enumerate(grid.each_row()):
            for ci, cell in enumerate(row):
                # Figure out the color
                if len(cell.links)>0:
                    color = grid.background_color_for(cell) if clr else (0,0,0)
                else:
                    color = (0,0,0) # no links therefore color cell
                # The entire cell
                rp, cp = ri*cs+1, ci*cs+1
                arr[rp:rp+cs, cp:cp+cs, 0] = color[0]
                arr[rp:rp+cs, cp:cp+cs, 1] = color[1]
                arr[rp:rp+cs, cp:cp+cs, 2] = color[2]
                # Corners of the cell
                arr[rp      ,cp      , 0:3] = 0
                arr[rp+cs-1 ,cp      , 0:3] = 0
                arr[rp      ,cp+cs-1 , 0:3] = 0
                arr[rp+cs-1 ,cp+cs-1 , 0:3] = 0
                # Walls
                if not cell.linked_to(cell.north): arr[rp          , cp+1:cp+cs-1, 0:3] = 0
                if not cell.linked_to(cell.south): arr[rp+cs-1     , cp+1:cp+cs-1, 0:3] = 0
                if not cell.linked_to(cell.west):  arr[rp+1:rp+cs-1, cp          , 0:3] = 0
                if not cell.linked_to(cell.east):  arr[rp+1:rp+cs-1, cp+cs-1     , 0:3] = 0
        return Image.fromarray(np.uint8(arr))

    @staticmethod
    def _processKwargs(**kwargs):
        ''' Process kwargs '''
        f = strftime("%Y%m%d%H%M%S", gmtime())
        cs = 4
        clr = False
        for key in kwargs:
            if key == 'filename':
                f = kwargs[key]
            elif key == 'cell_size':
                cs = kwargs[key]
            elif key == 'coloring':
                clr = kwargs[key]
        return f, cs, clr