from time import gmtime, strftime

import args
from typing import cast

from base.colored_grid import ColoredGrid

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath
from exporters.png_exporter import PNGExporter

from demos.demo_utils import ALGORITHMS, get_exporter, get_algorithm


DEFAULT_EXPORTER = "Wolf3DExporter"
AVAILABLE_EXPORTERS = ["Wolf3DExporter"]


def store_solution(grid: ColoredGrid) -> ColoredGrid:
    start_row, start_column, end_row, end_column = LongestPath.calculate(grid)
    solved_grid = cast(ColoredGrid, Dijkstra.calculate_distances(grid, start_row, start_column, end_row, end_column))
    return solved_grid


if __name__ == "__main__":
    if len(args.all) < 3:
        print("Usage:\nPYTHONPATH=. python3 demos/game_map_demo.py <rows> <columns> <algorithm> ", end="")
        print("[--exporter=<exporter>]")
        print("Valid algorithms: {}".format("|".join([algorithm.__name__ for algorithm in ALGORITHMS])))
        print("Valid exporters: {}".format("|".join(AVAILABLE_EXPORTERS)))
        exit(1)
    exporter, exporter_name = get_exporter(AVAILABLE_EXPORTERS, DEFAULT_EXPORTER)
    pathfinding = True
    rows = int(args.all[0])
    columns = int(args.all[1])
    algorithm = get_algorithm()
    print("Algorithm: {}\nRows: {}\ncolumns: {}\nExporter: {}".format(algorithm.__name__, rows, columns, exporter_name))

    valid_map = False
    while not valid_map:
        grid = ColoredGrid(rows, columns)
        grid = algorithm.on(grid)
        valid_map = exporter.is_valid(grid)
        if not valid_map:
            print("Generated maze has no east/west linked ending cell. Recreating...")

    filename = strftime("%d%H%M%S", gmtime())

    exporter.render(grid, filename=filename)

    print("Generated maze map has {} enemies".format(exporter.enemies_count))

    grid = store_solution(grid)
    PNGExporter().render(grid, coloring=True, filename=filename)
