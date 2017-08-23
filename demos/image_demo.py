import platform
import subprocess
from time import gmtime, strftime

import args
from typing import cast, Union     # noqa: F401

from base.grid import Grid
from base.distance_grid import DistanceGrid
from base.colored_grid import ColoredGrid

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

from utils.rotator import Rotator

from demos.demo_utils import ALGORITHMS, get_renderer, get_rotations, get_algorithm, get_pathfinding


DEFAULT_RENDERER = "PNGRenderer"
AVAILABLE_RENDERERS = ["PNGRenderer"]


def get_coloring() -> bool:
    return bool("--coloring" in args.flags)


if __name__ == "__main__":
    if len(args.all) < 3:
        print("Usage:\nPYTHONPATH=. python3 demos/image_demo.py <rows> <columns> <algorithm> ", end="")
        print("[--renderer=<renderer>] [--rotations=<rotations>] [--pathfinding] [--coloring]")
        print("Valid algorithms: {}".format("|".join([algorithm.__name__ for algorithm in ALGORITHMS])))
        print("Valid renderers: {}".format("|".join(AVAILABLE_RENDERERS)))
        print("Rotations is an integer value measuring number of 90 degree clockwise rotations to perform")
        print("Pathfinding flag shows distances between cells")
        exit(1)
    renderer, renderer_name = get_renderer(AVAILABLE_RENDERERS, DEFAULT_RENDERER)
    rotations = get_rotations()
    pathfinding = get_pathfinding()
    rows = int(args.all[0])
    columns = int(args.all[1])
    algorithm = get_algorithm()
    coloring = get_coloring()
    print("Algorithm: {}\nRows: {}\ncolumns: {}\nRenderer: {}".format(algorithm.__name__, rows, columns, renderer_name))
    print("90deg Rotations: {}\nPathfinding: {}\nColoring: {}".format(rotations, pathfinding, coloring))

    # here coloring takes precedence, because ColoredGrid inherits from DistanceGrid
    if coloring:
        grid = ColoredGrid(rows, columns)  # type: Union[Grid, DistanceGrid, ColoredGrid]
    elif pathfinding:
        grid = DistanceGrid(rows, columns)
    else:
        grid = Grid(rows, columns)

    grid = algorithm.on(grid)

    for num in range(rotations):
        grid = Rotator.on(grid)

    # here pathfinding first, so if also colored we'll see the route colored, else if colored will see all maze painted
    if pathfinding:
        start_row, start_column, end_row, end_column = LongestPath.calculate(cast(DistanceGrid, grid))
        print("Solving maze from row {} column {} to row {} column {}".format(
            start_row, start_column, end_row, end_column))
        grid = Dijkstra.calculate_distances(cast(DistanceGrid, grid), start_row, start_column, end_row, end_column)
    elif coloring:
        start_row = round(grid.rows / 2)
        start_column = round(grid.columns / 2)
        print("Drawing colored maze with start row {} column {}".format(start_row, start_column))
        start_cell = grid.cell_at(start_row, start_column)
        if start_cell is None:
            raise IndexError("Invalid start cell row {} column {}".format(start_row, start_column))
        grid.distances = start_cell.distances     # type: ignore

    filename = strftime("%Y%m%d%H%M%S", gmtime())

    renderer.render(grid, coloring=coloring, filename=filename)

    print("Maze has {} dead-ends".format(len(grid.deadends)))

    if platform.system() == "Linux":
        subprocess.run(["xdg-open", "{}.png".format(filename)])
