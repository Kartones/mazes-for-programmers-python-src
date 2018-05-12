import argparse
from time import gmtime, strftime
from typing import cast

from base.colored_grid import ColoredGrid
from exporters.png_exporter import PNGExporter
from exporters.wolf3d_exporter import Wolf3DExporter
import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

from demos.demo_utils import ALGORITHM_NAMES, get_algorithm, get_exporter


DEFAULT_EXPORTER = "Wolf3DExporter"
AVAILABLE_EXPORTERS = ["Wolf3DExporter"]
AVAILABLE_ALGORITHMS = ALGORITHM_NAMES


def store_solution(grid: ColoredGrid) -> ColoredGrid:
    start, end = LongestPath.calculate(grid)
    Dijkstra.calculate_distances(grid, start, end)
    return grid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a maze")
    parser.add_argument("rows", type=int, help="number of rows")
    parser.add_argument("columns", type=int, help="number of columns")
    parser.add_argument("algorithm", type=str, help="algorithm to use")
    parser.add_argument("-e", "--exporter", type=str, default=DEFAULT_EXPORTER, help="maze exporter to use")
    parser.add_argument("-f", "--filename", type=str, default=None, help="file name to use")
    args = parser.parse_args()

    rows = args.rows
    columns = args.columns
    algorithm = get_algorithm(args.algorithm, AVAILABLE_ALGORITHMS)
    exporter = cast(Wolf3DExporter, get_exporter(args.exporter, AVAILABLE_EXPORTERS))
    filename = strftime("%d%H%M%S", gmtime())

    print("Algorithm: {}\nRows: {}\ncolumns: {}\nExporter: {}".format(args.algorithm, rows, columns, args.exporter))

    valid_map = False
    while not valid_map:
        grid = ColoredGrid(rows, columns)
        algorithm.on(grid)
        valid_map = exporter.is_valid(grid)
        if not valid_map:
            print("Generated maze has no east/west linked ending cell. Recreating...")

    exporter.render(grid, filename=filename)

    print("Generated maze map has {} enemies".format(exporter.enemies_count))

    grid = store_solution(grid)
    PNGExporter().render(grid, coloring=True, filename=filename)
