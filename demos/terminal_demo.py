import args
from typing import cast, Union     # noqa: F401

from base.grid import Grid
from base.distance_grid import DistanceGrid

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

from utils.rotator import Rotator

from demos.demo_utils import ALGORITHMS, get_exporter, get_rotations, get_algorithm, get_pathfinding


DEFAULT_EXPORTER = "UnicodeExporter"
AVAILABLE_EXPORTERS = ["ASCIIExporter", "UnicodeExporter"]


if __name__ == "__main__":
    if len(args.all) < 3:
        print("Usage:\nPYTHONPATH=. python3 demos/terminal_demo.py <rows> <columns> <algorithm> ", end="")
        print("[--exporter=<exporter>] [--rotations=<rotations>] [--pathfinding]")
        print("Valid algorithms: {}".format("|".join([algorithm.__name__ for algorithm in ALGORITHMS])))
        print("Valid exporters: {}".format("|".join(AVAILABLE_EXPORTERS)))
        print("Rotations is an integer value measuring number of 90 degree clockwise rotations to perform")
        print("Pathfinding flag shows distances between cells")
        exit(1)
    exporter, exporter_name = get_exporter(AVAILABLE_EXPORTERS, DEFAULT_EXPORTER)
    rotations = get_rotations()
    pathfinding = get_pathfinding()
    rows = int(args.all[0])
    columns = int(args.all[1])
    algorithm = get_algorithm()
    print("Algorithm: {}\nRows: {}\ncolumns: {}\nExporter: {}".format(algorithm.__name__, rows, columns, exporter_name))
    print("90deg Rotations: {}\nPathfinding: {}".format(rotations, pathfinding))

    if pathfinding:
        grid = DistanceGrid(rows, columns)  # type: Union[Grid, DistanceGrid]
    else:
        grid = Grid(rows, columns)

    grid = algorithm.on(grid)

    for num in range(rotations):
        grid = Rotator.on(grid)

    if pathfinding:
        start_row, start_column, end_row, end_column = LongestPath.calculate(cast(DistanceGrid, grid))
        print("Solving maze from row {} column {} to row {} column {}".format(
            start_row, start_column, end_row, end_column))
        grid = Dijkstra.calculate_distances(cast(DistanceGrid, grid), start_row, start_column, end_row, end_column)

    exporter.render(grid)

    print("Maze has {} dead-ends".format(len(grid.deadends)))
