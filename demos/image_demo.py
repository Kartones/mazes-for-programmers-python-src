import argparse
from time import gmtime, strftime
from typing import cast

from base.colored_grid import ColoredGrid
from base.rotator import Rotator

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

from demos.demo_utils import ALGORITHM_NAMES, str2bool, get_algorithm, get_exporter


DEFAULT_EXPORTER = "PNGExporter"
AVAILABLE_EXPORTERS = ["PNGExporter"]
AVAILABLE_ALGORITHMS = ALGORITHM_NAMES


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a maze")
    parser.add_argument("rows", type=int, help="number of rows")
    parser.add_argument("columns", type=int, help="number of columns")
    parser.add_argument("algorithm", type=str, help="algorithm to use")
    parser.add_argument("-e", "--exporter", type=str, default=DEFAULT_EXPORTER, help="maze exporter to use")
    parser.add_argument("-f", "--filename", type=str, default=None, help="file name to use")
    parser.add_argument("-r", "--rotations", type=int, default=0,
                        help="number of 90 degree clockwise rotations to perform")
    parser.add_argument("-p", "--pathfinding", type=str2bool, default=False, help="whether solve the maze")
    parser.add_argument("-c", "--coloring", type=str2bool, help="whether to color the maze solution")
    args = parser.parse_args()

    rows = args.rows
    columns = args.columns
    algorithm = get_algorithm(args.algorithm, AVAILABLE_ALGORITHMS)
    exporter = get_exporter(args.exporter, AVAILABLE_EXPORTERS)
    filename = args.filename if args.filename else strftime("%Y%m%d%H%M%S", gmtime())
    rotations = args.rotations
    pathfinding = args.pathfinding
    coloring = args.coloring
    print("Algorithm: {}\nRows: {}\ncolumns: {}\nExporter: {}".format(args.algorithm, rows, columns, args.exporter))
    print("90deg Rotations: {}\nPathfinding: {}\nColoring: {}".format(rotations, pathfinding, coloring))

    # Always use Colored Grid. Just don"t color the output if colored == False
    grid = ColoredGrid(rows, columns)

    algorithm.on(grid)

    for num in range(rotations):
        grid = cast(ColoredGrid, Rotator().on(grid))

    # here pathfinding first, so if also colored we"ll see the route colored, else if colored will see all maze painted
    if pathfinding:
        start, end = LongestPath.calculate(grid)
        print("Solving maze from row {} column {} to row {} column {}".format(*start, *end))
        Dijkstra.calculate_distances(grid, start, end)
    elif coloring:
        starting_position = (round(grid.rows / 2), round(grid.columns / 2))
        print("Drawing colored maze with start row {} column {}".format(*starting_position))
        if grid[starting_position] is None:
            raise IndexError("Invalid start cell row {} column {}".format(*starting_position))
        grid.distances = grid[starting_position].distances  # type: ignore

    exporter.render(grid, coloring=coloring, filename=filename)

    print("Maze has {} dead-ends".format(len(grid.deadends)))
