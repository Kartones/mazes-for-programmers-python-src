from typing import Any, cast

from base.cell import Cell
from base.grid import Grid

# if not linked/closed, add that side's value to find position at array:
#    N        1
#  W   E    2   4
#    S        8

JUNCTIONS = [" ", " ", " ", "\u251b", " ", "\u2517", "\u2501", "\u253b", " ", "\u2503", "\u2513", "\u252b", "\u250f",
             "\u2523", "\u2533", "\u254b"]

NORTH = 1
WEST = 2
EAST = 4
SOUTH = 8


def render(grid: Grid, **kwargs: Any) -> None:
        """
        Renders to stdout a UNICODE representation of the maze.
        Not present in the book but suggested as exercise. And looks better than ASCII mazes :)
        """
        horizontal_wall = "\u2501"
        vertical_wall = "\u2503"

        output = JUNCTIONS[12]
        for x in range(grid.columns - 1):
            output += (horizontal_wall * 3 + get_topmost_junction(cast(Cell, grid.get_cell(row=0, column=x))))
        output += horizontal_wall * 3 + JUNCTIONS[10] + "\n"

        for row in grid.each_row():
            top = vertical_wall
            bottom = get_leftmost_junction(row[0])
            for cell in row:
                body = grid.contents_of(cell)
                east_boundary = " " if cell.linked_to(cell.east) else vertical_wall
                top += body + east_boundary
                south_boundary = "   " if cell.linked_to(cell.south) else horizontal_wall * 3
                bottom += south_boundary + get_south_east_junction(cell)
            output += top + "\n"
            output += bottom + "\n"

        print(output)


def get_leftmost_junction(cell: Cell) -> str:
    #
    #    [ X ]
    #
    #  [ X-south]
    #
    junction = NORTH

    if cell.south:
        junction += SOUTH
        if not cell.linked_to(cell.south):
            junction += EAST
    else:
        junction += EAST

    return JUNCTIONS[junction]


def get_topmost_junction(cell: Cell) -> str:
    # special case for 1st row's junctions
    #
    #    [ X ]      [X-east]
    #
    junction = EAST + WEST

    if not cell.linked_to(cast(Cell, cell.east)):
        junction += SOUTH

    return JUNCTIONS[junction]


def get_south_east_junction(cell: Cell) -> str:
    # Taking advantage that we always go forward     east and south, just need to calculate available posibilities
    #
    #    [ X ]      [X-east]
    #
    #  [ X-south] [X-southeast]
    #
    junction = 0

    if cell.east:
        if not cell.linked_to(cell.east):
            junction += NORTH
        if not cell.east.south:
            junction += EAST
    else:
        junction += NORTH

    if cell.south:
        if not cell.linked_to(cell.south):
            junction += WEST
        if not cell.south.east:
            junction += SOUTH
    else:
        junction += WEST

    if cell.east and cell.south:
        south_east_cell = cast(Cell, cell.south.east)
        if not cell.east.linked_to(south_east_cell):
            junction += EAST
        if not cell.south.linked_to(south_east_cell):
            junction += SOUTH
    try:
        return JUNCTIONS[junction]
    except IndexError as ie:
        print("junction:{} error:{}".format(junction, ie))
        return " "
