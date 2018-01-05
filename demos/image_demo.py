# Temporarilly add parent folder to path (if not already added)
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from platform import system
from subprocess import run
from time import gmtime, strftime

import argparse
from typing import cast

from base.grid import Grid
from base.distance_grid import DistanceGrid
from base.colored_grid import ColoredGrid

from pathfinders import dijkstra as Dijkstra
from pathfinders import longest_path as LongestPath

from utils.rotator import Rotator

from demos.demo_utils import ALGORITHM_NAMES, str2bool, avalible_algorithm, avalible_exporter

DEFAULT_EXPORTER = 'PNGExporter'
AVAILABLE_EXPORTERS = ['PNGExporter','PixelExporter']
AVAILABLE_ALGORITHMS = ALGORITHM_NAMES

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Render a maze')
    parser.add_argument('rows', type=int, help='number or rows')
    parser.add_argument('cols', type=int, help='number or columns')
    parser.add_argument('algorithm', type=str, help='algorithm to use')
    parser.add_argument('-e', '--exporter', type=str, default=DEFAULT_EXPORTER, help='maze exporter to use')
    parser.add_argument('-f', '--filename', type=str, default=None, help='file name to use')
    parser.add_argument('-r', '--rotations', type=int, default=0, help='integer value measuring number of 90 degree clockwise rotations to perform')
    parser.add_argument('-p', '--pathfinding', type=str2bool, default=False, help='whether to find the path through the maze')
    parser.add_argument('-c', '--coloring', type=str2bool, help='whether to color the maze')
    args = parser.parse_args()

    rows = args.rows
    cols = args.cols
    algorithm = avalible_algorithm(args.algorithm, AVAILABLE_ALGORITHMS)
    exporter = avalible_exporter(args.exporter, AVAILABLE_EXPORTERS)
    filename = args.filename if args.filename else strftime('%Y%m%d%H%M%S', gmtime())
    rotations = args.rotations
    pathfinding = args.pathfinding
    coloring = args.coloring
    print('Algorithm: {}\nRows: {}\ncolumns: {}\nExporter: {}'.format(args.algorithm, rows, cols, args.exporter))
    print('90deg Rotations: {}\nPathfinding: {}\nColoring: {}'.format(rotations, pathfinding, coloring))

    # Always use Colored Grid. Just don't color the output if colored == False
    grid = ColoredGrid(rows, cols)

    algorithm().on(grid)

    for num in range(rotations):
        grid = Rotator.on(grid)

    exporter.render(grid, coloring=coloring, filename=filename)

    # here pathfinding first, so if also colored we'll see the route colored, else if colored will see all maze painted
    if pathfinding:
        start_row, start_column, end_row, end_column = LongestPath.calculate(grid)
        print('Solving maze from row {} column {} to row {} column {}'.format(
            start_row, start_column, end_row, end_column))
        grid = Dijkstra.calculate_distances(grid, start_row, start_column, end_row, end_column)
    elif coloring:
        start_row = round(grid.rows / 2)
        start_column = round(grid.cols / 2)
        print('Drawing colored maze with start row {} column {}'.format(start_row, start_column))
        start_cell = grid[start_row, start_column]
        if start_cell is None:
            raise IndexError('Invalid start cell row {} column {}'.format(start_row, start_column))
        grid.distances = start_cell.distances     # type: ignore

    exporter.render(grid, coloring=coloring, filename=filename + '_col')

    print('Maze has {} dead-ends'.format(len(grid.deadends)))

    if system() == 'Linux':
        run(['xdg-open', '{}.png'.format(filename)])
