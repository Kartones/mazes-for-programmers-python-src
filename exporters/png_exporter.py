from time import gmtime, strftime
from typing import Any, Tuple

from PIL import Image, ImageDraw

from base.colored_grid import ColoredGrid
from base.grid import Grid
from exporters.exporter import Exporter


class PNGExporter(Exporter):

    def render(self, grid: Grid, **kwargs: Any) -> None:
        hasColor = isinstance(grid, ColoredGrid)
        filename, cell_size, coloring = self._processKwargs(**kwargs)
        image = self._render(grid, cell_size, coloring and hasColor)
        image.save('{}.png'.format(filename), 'PNG', optimize=True)

    @staticmethod
    def _render(grid: Grid, cell_size: int=4, coloring: bool=False) -> Image:
        ''' Rendering core '''
        wall_color = (0, 0, 0)
        image = Image.new('RGBA', (cell_size * grid.cols + 1, cell_size * grid.rows + 1), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        for draw_pass in range(2):
            for cell in grid.eachCell():
                x1 = cell.col * cell_size
                y1 = cell.row * cell_size
                x2 = (cell.col + 1) * cell_size
                y2 = (cell.row + 1) * cell_size

                if draw_pass == 0:
                    color = grid.color(cell) if coloring else (255, 255, 255)  # type: ignore
                    draw.rectangle((x1, y1, x2, y2), fill=color)
                else:
                    if not cell.north:        draw.line((x1, y1, x2, y1), fill=wall_color, width=1)
                    if not cell.west:         draw.line((x1, y1, x1, y2), fill=wall_color, width=1)
                    if not cell & cell.east:  draw.line((x2, y1, x2, y2), fill=wall_color, width=1)
                    if not cell & cell.south: draw.line((x1, y2, x2, y2), fill=wall_color, width=1)
        return image

    @staticmethod
    def _processKwargs(**kwargs: Any) -> Tuple[str, int, bool]:
        filename = strftime('%Y%m%d%H%M%S', gmtime())
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
