# Temporarilly add parent folder to path (if not already added)
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
import platform
import subprocess
from time import gmtime, strftime

import argparse
from typing import cast

from base.colored_grid import ColoredGrid

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

from exporters.png_exporter import PNGExporter

from demos.demo_utils import ALGORITHM_NAMES, str2bool, avalible_algorithm, avalible_exporter


DEFAULT_EXPORTER = "Wolf3DExporter"
AVAILABLE_EXPORTERS = ["Wolf3DExporter"]
AVAILABLE_ALGORITHMS = ALGORITHM_NAMES

def store_solution(grid: ColoredGrid) -> ColoredGrid:
    start_row, start_column, end_row, end_column = LongestPath.calculate(grid)
    solved_grid = cast(ColoredGrid, Dijkstra.calculate_distances(grid, start_row, start_column, end_row, end_column))
    return solved_grid

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Render a maze')
    parser.add_argument('rows', type=int, help='number or rows')
    parser.add_argument('cols', type=int, help='number or columns')
    parser.add_argument('algorithm', type=str, help='algorithm to use')
    parser.add_argument('-e', '--exporter', type=str, default=DEFAULT_EXPORTER, help='maze exporter to use')
    parser.add_argument('-f', '--filename', type=str, default=None, help='file name to use')
    args = parser.parse_args()

    rows = args.rows
    cols = args.cols
    algorithm = avalible_algorithm(args.algorithm, AVAILABLE_ALGORITHMS)
    exporter = avalible_exporter(args.exporter, AVAILABLE_EXPORTERS)
    filename = args.filename if args.filename else strftime("%Y%m%d%H%M%S", gmtime())

    print("Algorithm: {}\nRows: {}\ncolumns: {}\nExporter: {}".format(args.algorithm, rows, cols, args.exporter))

    valid_map = False
    while not valid_map:
        grid = ColoredGrid(rows, cols)
        grid = algorithm.on(grid)
        valid_map = exporter.is_valid(grid)
        if not valid_map:
            print("Generated maze has no east/west linked ending cell. Recreating...")

    exporter.render(grid, filename=filename)

    print("Generated maze map has {} enemies".format(exporter.enemies_count))

    grid = store_solution(grid)
    PNGExporter().render(grid, coloring=True, filename=filename)

    if platform.system() == "Linux":
        subprocess.run(["xdg-open", "{}.png".format(filename)])
