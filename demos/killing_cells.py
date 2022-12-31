import argparse
from itertools import chain
import random
from typing import Any, cast

from base.distance_grid import DistanceGrid
from base.masked_grid import MaskedGrid
from base.rotator import Rotator
from base.mask import Mask

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

from demos.demo_utils import ALGORITHM_NAMES, str2bool, get_algorithm, get_exporter


DEFAULT_EXPORTER = "UnicodeExporter"
AVAILABLE_EXPORTERS = ["ASCIIExporter", "UnicodeExporter"]
AVAILABLE_ALGORITHMS = ALGORITHM_NAMES


if __name__ == "__main__":
    random.seed(10)
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
    algorithm = get_algorithm(args.algorithm, AVAILABLE_ALGORITHMS)
    exporter = get_exporter(args.exporter, AVAILABLE_EXPORTERS)
    rotations = args.rotations
    pathfinding = args.pathfinding
    print("Algorithm: {}\nRows: {}\ncolumns: {}\nExporter: {}".format(args.algorithm, rows, columns, args.exporter))
    print("90deg Rotations: {}\nPathfinding: {}".format(rotations, pathfinding))

    mask = Mask(rows, columns)
    # print("MASK")
    # print(mask.count())
    # print(mask.random_cell())

    grid = MaskedGrid(mask)
    # grid = DistanceGrid(rows, columns)
    # grid.cell_at(0, 9).west.east = None
    # grid.cell_at(0, 9).south.north = None
    # r: Any
    # for row in grid.each_row():
    #     print("ROW3")
    #     print(row)
    #     r = row

    # for cell in grid.each_cell_in_row(r):
    #     print("CELLx")
    #     print(cell)

    # for cell in chain(grid.each_cell()):
    #     print("CELL3")
    #     print(cell)


    algorithm.on(grid)

    for num in range(rotations):
        grid = cast(DistanceGrid, Rotator().on(grid))

    if pathfinding:
        start, end = LongestPath.calculate(grid)
        print("Solving maze from row {} column {} to row {} column {}".format(*start, *end))
        Dijkstra.calculate_distances(grid, start, end)

    exporter.render(grid)

    print("Maze has {} dead-ends".format(len(grid.deadends)))
