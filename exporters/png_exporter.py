from time import gmtime, strftime
from PIL import Image, ImageDraw
from typing import Any, TYPE_CHECKING, Union

from exporters.base_exporter import BaseExporter
from base.colored_grid import ColoredGrid
if TYPE_CHECKING:
    from base.grid import Grid  # noqa: F401


class PNGExporter(BaseExporter):

    def render(self, grid: Union["Grid", ColoredGrid], **kwargs: Any) -> None:
        assert isinstance(grid, ColoredGrid)
        filename, cell_size, coloring = self._processKwargs(**kwargs)
        image = self._render(grid, cell_size, coloring)
        image.save("{}.png".format(filename), "PNG", optimize=True)

    @staticmethod
    def _render(grid, cell_size:int=4, coloring:bool=False) -> Image:
        ''' Rendering core '''
        wall_color = (0, 0, 0)
        image = Image.new("RGBA", (cell_size*grid.cols + 1, cell_size*grid.rows + 1), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        for draw_pass in range(2):
            for cell in grid.each_cell():
                x1 = cell.col * cell_size
                y1 = cell.row * cell_size
                x2 = (cell.col + 1) * cell_size
                y2 = (cell.row + 1) * cell_size

                if draw_pass == 0 and coloring:
                    color = grid.background_color_for(cell)
                    draw.rectangle((x1, y1, x2, y2), fill=color)
                else:
                    if not cell.north:
                        draw.line((x1, y1, x2, y1), fill=wall_color, width=1)
                    if not cell.west:
                        draw.line((x1, y1, x1, y2), fill=wall_color, width=1)
                    if not cell.linked_to(cell.east):
                        draw.line((x2, y1, x2, y2), fill=wall_color, width=1)
                    if not cell.linked_to(cell.south):
                        draw.line((x1, y2, x2, y2), fill=wall_color, width=1)
        return image

    @staticmethod
    def _processKwargs(**kwargs):
        ''' Process kwargs '''
        filename = strftime("%Y%m%d%H%M%S", gmtime())
        cell_size = 4
        coloring = False
        for key in kwargs:
            if key == 'filename':
                filename = kwargs[key]
            elif key == 'cell_size':
                cell_size = kwargs[key]
            elif key == 'coloring':
                coloring = kwargs[key]
        return filename, cell_size, coloring