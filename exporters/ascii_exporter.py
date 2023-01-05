from typing import Any

from exporters.base_exporter import Exporter
from base.grid import Grid


class ASCIIExporter(Exporter):
    """
    Renders to stdout an ASCII representation of the maze.
    Rendering starts with top walls and nortwest corner setup, so it only needs to care of each cell's east and
    south walls.
    """

    def render(self, grid: Grid, **kwargs: Any) -> None:

        for level in grid.each_level():
            output = "+" + "---+" * grid.columns + "\n"
            for row in grid.each_row_in_level(level):
                top = "|"
                bottom = "+"
                for cell in grid.each_cell_in_row(row):
                    # NOTE: Book here creates dummy (-1,-1) cell. Not doing it until needed
                    body = grid.contents_of(cell)
                    if cell.linked_to(cell.up) and cell.linked_to(cell.down):
                        body += "*"
                    elif cell.linked_to(cell.up):
                        body += "^"
                    elif cell.linked_to(cell.down):
                        body += "."
                    else:
                        body += " "
                    east_boundary = " " if cell.linked_to(cell.east) else "|"
                    top += body + east_boundary
                    south_boundary = "   " if cell.linked_to(cell.south) else "---"
                    corner = "+"
                    bottom += south_boundary + corner
                output += top + "\n"
                output += bottom + "\n"

            print(output)
