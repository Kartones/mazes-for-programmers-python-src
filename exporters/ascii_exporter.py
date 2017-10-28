from typing import Any

from exporters.base_exporter import BaseExporter
from base.grid import Grid


class ASCIIExporter(BaseExporter):
    """
    Renders to stdout an ASCII representation of the maze.
    Rendering starts with top walls and nortwest corner setup, so it only needs to care of each cell's east and
    south walls.
    """

    def render(self, grid: Grid, **kwargs: Any) -> None:
        output = "+" + "---+" * grid.columns + "\n"

        for row in grid.each_row():
            top = "|"
            bottom = "+"
            for cell in row:
                # NOTE: Book here creates dummy (-1,-1) cell. Not doing it until needed
                body = grid.contents_of(cell)
                east_boundary = " " if cell.linked_to(cell.east) else "|"
                top += body + east_boundary
                south_boundary = "   " if cell.linked_to(cell.south) else "---"
                corner = "+"
                bottom += south_boundary + corner
            output += top + "\n"
            output += bottom + "\n"

        print(output)
