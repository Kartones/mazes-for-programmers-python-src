from base.grid import Grid


def render(grid: Grid) -> None:
    """
    Renders to stdout an ASCII representation of the maze.
    Rendering starts with top walls and nortwest corner setup, so it only needs to care of each cell's east and
    south walls.
    """

    output = "+" + "---+" * grid.columns + "\n"

    for row in grid.each_row():
        top = "|"
        bottom = "+"
        for cell in row:
            # NOTE: Book here creates dummy (-1,-1) cell. Not doing it until needed
            body = "   "
            east_boundary = " " if cell.linked_to(cell.east) else "|"
            top += body + east_boundary
            south_boundary = "   " if cell.linked_to(cell.south) else "---"
            corner = "+"
            bottom += south_boundary + corner
        output += top + "\n"
        output += bottom + "\n"

    print(output)
