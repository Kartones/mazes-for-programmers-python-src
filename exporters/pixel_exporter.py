from time import gmtime, strftime
from typing import TYPE_CHECKING, Any, Union

import numpy as np
from PIL import Image, ImageDraw

from base.colored_grid import ColoredGrid
from base.grid import Grid  # noqa: F401
from exporters.exporter import Exporter


class PixelExporter(Exporter):
    ''' Export grid into a pixel-perfect image '''

    def render(self, grid: Union["Grid", ColoredGrid], **kwargs: Any) -> None:
        ''' Main render method '''
        assert isinstance(grid, ColoredGrid)
        filename, cell_size, coloring = self._processKwargs(**kwargs)
        image = self._render(grid, cell_size, coloring)
        image.save("{}.png".format(filename), "PNG", optimize=True)

    @staticmethod
    def _render(grid, cell_size:int=4, coloring:bool=False) -> Image:
        ''' Rendering core '''
        cs = cell_size
        arr = np.zeros((cs*grid.rows+2, cs*grid.cols+2, 3))
        # Outermost walls
        arr[ :, 0,0:3] = 0
        arr[ :,-1,0:3] = 0
        arr[ 0, :,0:3] = 0
        arr[-1, :,0:3] = 0
        # Draw each cell
        for ri, row in enumerate(grid.eachRow()):
            for ci, cell in enumerate(row):
                # Figure out the color
                if len(cell.links)>0:
                    color = grid.color(cell) if coloring else (0,0,0)
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
                if not cell & cell.north: arr[rp          , cp+1:cp+cs-1, 0:3] = 0
                if not cell & cell.south: arr[rp+cs-1     , cp+1:cp+cs-1, 0:3] = 0
                if not cell & cell.west:  arr[rp+1:rp+cs-1, cp          , 0:3] = 0
                if not cell & cell.east:  arr[rp+1:rp+cs-1, cp+cs-1     , 0:3] = 0
        return Image.fromarray(np.uint8(arr))

    @staticmethod
    def _processKwargs(**kwargs):
        ''' Process kwargs '''
        filename = strftime("%Y%m%d%H%M%S", gmtime())
        cell_size = 4
        coloring = False
        for key in kwargs:
            if key == 'filename':
                f = kwargs[key]
            elif key == 'cell_size':
                cell_size = kwargs[key]
            elif key == 'coloring':
                coloring = kwargs[key]
        return filename, cell_size, coloring
