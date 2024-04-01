from time import gmtime, strftime
from typing import Any, cast, Tuple

from PIL import Image, ImageDraw
from PIL.Image import Image as ImageType

from exporters.base_exporter import Exporter
from base.colored_grid import ColoredGrid
from base.grid import Grid


STEP_BACKGROUND = 0


class PNGExporter(Exporter):

    def render(self, grid: Grid, **kwargs: Any) -> None:
        has_color = isinstance(grid, ColoredGrid)

        filename, cell_size, coloring = self._process_kwargs(**kwargs)
        image = self._render(grid, cell_size, coloring and has_color)
        image.save("{}.png".format(filename), "PNG", optimize=True)

    @staticmethod
    def _render(grid: Grid, cell_size: int = 4, coloring: bool = False) -> ImageType:
        wall_color = (0, 0, 0)
        image_width = cell_size * grid.columns
        image_height = cell_size * grid.rows

        image = Image.new("RGBA", (image_width + 1, image_height + 1), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        for draw_pass in range(2):
            for cell in grid.each_cell():
                x1 = cell.column * cell_size
                y1 = cell.row * cell_size
                x2 = (cell.column + 1) * cell_size
                y2 = (cell.row + 1) * cell_size

                if draw_pass == STEP_BACKGROUND and coloring:
                    if coloring:
                        color = cast(ColoredGrid, grid).background_color_for(cell)
                    else:
                        color = (255, 255, 255)
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
    def _process_kwargs(**kwargs: Any) -> Tuple[str, int, bool]:
        filename = strftime("%Y%m%d%H%M%S", gmtime())
        cell_size = 10
        coloring = False
        for key in kwargs:
            if key == "filename":
                filename = kwargs[key]
            elif key == "cell_size":
                cell_size = kwargs[key]
            elif key == "coloring":
                coloring = kwargs[key]
        return filename, cell_size, coloring

# ----
