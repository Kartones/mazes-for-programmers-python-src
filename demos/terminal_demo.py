import argparse
from typing import cast

from base.distance_grid import DistanceGrid
from base.grid3d import Grid3d
from base.rotator import Rotator

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

from demos.demo_utils import ALGORITHM_NAMES, str2bool, get_algorithm, get_exporter


DEFAULT_EXPORTER = "UnicodeExporter"
AVAILABLE_EXPORTERS = ["ASCIIExporter", "UnicodeExporter"]
AVAILABLE_ALGORITHMS = ALGORITHM_NAMES


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a maze")
    parser.add_argument("levels", type=int, help="number of levels")
    parser.add_argument("rows", type=int, help="number of rows")
    parser.add_argument("columns", type=int, help="number of columns")
    parser.add_argument("algorithm", type=str, help="algorithm to use")
    parser.add_argument("-e", "--exporter", type=str, default=DEFAULT_EXPORTER, help="maze exporter to use")
    parser.add_argument("-r", "--rotations", type=int, default=0,
                        help="number of 90 degree clockwise rotations to perform")
    parser.add_argument("-p", "--pathfinding", type=str2bool, default=False, help="whether solve the maze")
    args = parser.parse_args()

    levels = args.levels
    rows = args.rows
    columns = args.columns
    algorithm = get_algorithm(args.algorithm, AVAILABLE_ALGORITHMS)
    exporter = get_exporter(args.exporter, AVAILABLE_EXPORTERS)
    rotations = args.rotations
    pathfinding = args.pathfinding
    print("Algorithm: {}\nLevels: {}\nRows: {}\ncolumns: {}\nExporter: {}".format(args.algorithm, levels, rows, columns, args.exporter))
    print("90deg Rotations: {}\nPathfinding: {}".format(rotations, pathfinding))

    grid = Grid3d(levels, rows, columns)
    algorithm.on(grid)
    grid.braid(.5)

    for num in range(rotations):
        grid = cast(DistanceGrid, Rotator().on(grid))

    if pathfinding:
        start, end = LongestPath.calculate(grid)
        print("Solving maze from level {} row {} column {} to level {} row {} column {}".format(*start, *end))
        Dijkstra.calculate_distances(grid, start, end)

    exporter.render(grid)

    print("Maze has {} dead-ends".format(len(grid.deadends)))
