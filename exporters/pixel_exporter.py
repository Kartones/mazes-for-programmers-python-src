from time import gmtime, strftime
from typing import TYPE_CHECKING, Any, Union

import numpy as np
from PIL import Image, ImageDraw

from base.colored_grid import ColoredGrid
from exporters.base_exporter import BaseExporter

if TYPE_CHECKING:
    from base.grid import Grid  # noqa: F401


class PixelExporter(BaseExporter):
    def render(self, grid: Union["Grid", ColoredGrid], **kwargs: Any) -> None:
        assert isinstance(grid, ColoredGrid)

        filename = strftime("%Y%m%d%H%M%S", gmtime())
        cs = 4
        coloring = False
        save = True

        for key in kwargs:
            if key == 'filename':
                filename = kwargs[key]
            elif key == 'cell_size':
                cs = kwargs[key]
            elif key == 'coloring':
                coloring = kwargs[key]
            elif key == 'save':
                save = kwargs[key] 

        wall_color = (0, 0, 0)
        arr = np.ones((cs*grid.rows+2, cs*grid.columns+2, 4))

        # Outermost walls
        arr[ :, 0,0:3] = 0
        arr[ :,-1,0:3] = 0
        arr[ 0, :,0:3] = 0
        arr[-1, :,0:3] = 0

        for ri, row in enumerate(grid.each_row()):
            for ci, cell in enumerate(row):
                # Figure out colors
                if len(cell.links)>0:
                    color = grid.background_color_for(cell) if coloring else (0,0,0)
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

        image = Image.fromarray(np.uint8(arr*255))
        if save:
            image.save("{}.png".format(filename), "PNG", optimize=True)
        else:
            return image
