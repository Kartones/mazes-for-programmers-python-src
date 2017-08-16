from PIL import Image, ImageDraw
from time import gmtime, strftime

from base.grid import Grid


class PNGRenderer:

    @staticmethod
    def render(grid: Grid, cell_size: int = 10, filename: str = None) -> None:
        if filename is None:
            filename = strftime("%Y%m%d%H%M%S", gmtime())

        image_width = cell_size * grid.columns
        image_height = cell_size * grid.rows

        wall_color = "black"

        image = Image.new("RGBA", (image_width + 1, image_height + 1), "white")

        draw = ImageDraw.Draw(image)

        for cell in grid.each_cell():
            x1 = cell.column * cell_size
            y1 = cell.row * cell_size
            x2 = (cell.column + 1) * cell_size
            y2 = (cell.row + 1) * cell_size

            if not cell.north:
                draw.line((x1, y1, x2, y1), fill=wall_color, width=1)
            if not cell.west:
                draw.line((x1, y1, x1, y2), fill=wall_color, width=1)
            if not cell.linked_to(cell.east):
                draw.line((x2, y1, x2, y2), fill=wall_color, width=1)
            if not cell.linked_to(cell.south):
                draw.line((x1, y2, x2, y2), fill=wall_color, width=1)

        image.save("{}.png".format(filename), "PNG", optimize=True)


# -----
# Unused at least for now: Pixel-based drawing:
# pixels = img.load()
# for x in range(img.size[0]):
#     for y in range(img.size[1]):
#         pixels[x, y] = (x, y, 100)
