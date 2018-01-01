from typing import TYPE_CHECKING, Any

from base.grid import Grid
from exporters.exporter import Exporter

class ASCIIExporter(Exporter):
    """
    Renders to stdout an ASCII representation of the maze.
    Rendering starts with top walls and nortwest corner setup, so it only needs to care of each cell's east and
    south walls.
    """

    def render(self, grid: Grid, **kwargs: Any) -> None:
        output = "+" + "---+" * grid.cols + "\n"

        for row in grid.eachRow():
            top = "|"
            bottom = "+"
            for cell in row:
                # NOTE: Book here creates dummy (-1,-1) cell. Not doing it until needed
                body = grid.contents(cell)
                east_boundary = " " if cell & cell.east else "|"
                top += body + east_boundary
                south_boundary = "   " if cell & cell.south else "---"
                corner = "+"
                bottom += south_boundary + corner
            output += top + "\n"
            output += bottom + "\n"

        print(output)
