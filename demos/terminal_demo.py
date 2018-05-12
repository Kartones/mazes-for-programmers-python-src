import argparse
from typing import cast

from base.distance_grid import DistanceGrid
from base.rotator import Rotator

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

from demos.demo_utils_v2 import ALGORITHM_NAMES, str2bool, available_algorithm, available_exporter


DEFAULT_EXPORTER = "UnicodeExporter"
AVAILABLE_EXPORTERS = ["ASCIIExporter", "UnicodeExporter"]
AVAILABLE_ALGORITHMS = ALGORITHM_NAMES


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a maze")
    parser.add_argument("rows", type=int, help="number of rows")
    parser.add_argument("columns", type=int, help="number of columns")
    parser.add_argument("algorithm", type=str, help="algorithm to use")
    parser.add_argument("-e", "--exporter", type=str, default=DEFAULT_EXPORTER, help="maze exporter to use")
    parser.add_argument("-r", "--rotations", type=int, default=0,
                        help="number of 90 degree clockwise rotations to perform")
    parser.add_argument("-p", "--pathfinding", type=str2bool, default=False, help="whether solve the maze")
    args = parser.parse_args()

    rows = args.rows
    columns = args.columns
    algorithm = available_algorithm(args.algorithm, AVAILABLE_ALGORITHMS)
    exporter = available_exporter(args.exporter, AVAILABLE_EXPORTERS)
    rotations = args.rotations
    pathfinding = args.pathfinding
    print("Algorithm: {}\nRows: {}\ncolumns: {}\nExporter: {}".format(args.algorithm, rows, columns, args.exporter))
    print("90deg Rotations: {}\nPathfinding: {}".format(rotations, pathfinding))

    grid = DistanceGrid(rows, columns)
    algorithm.on(grid)

    for num in range(rotations):
        grid = cast(DistanceGrid, Rotator().on(grid))

    if pathfinding:
        start, end = LongestPath.calculate(grid)
        print("Solving maze from row {} column {} to row {} column {}".format(*start, *end))
        Dijkstra.calculate_distances(grid, start, end)

    exporter.render(grid)

    print("Maze has {} dead-ends".format(len(grid.deadends)))
