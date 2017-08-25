import platform
import subprocess
from time import gmtime, strftime

import args
from typing import cast

from base.colored_grid import ColoredGrid

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath
import renderers.png_renderer as PNGRenderer

from demos.demo_utils import ALGORITHMS, renderer, get_algorithm


DEFAULT_RENDERER = "Wolf3DRenderer"
AVAILABLE_RENDERERS = ["Wolf3DRenderer"]


def store_solution(grid: ColoredGrid) -> ColoredGrid:
    start_row, start_column, end_row, end_column = LongestPath.calculate(grid)
    grid = cast(ColoredGrid, Dijkstra.calculate_distances(grid, start_row, start_column, end_row, end_column))
    return grid


if __name__ == "__main__":
    if len(args.all) < 3:
        print("Usage:\nPYTHONPATH=. python3 demos/game_map_demo.py <rows> <columns> <algorithm> ", end="")
        print("[--renderer=<renderer>]")
        print("Valid algorithms: {}".format("|".join([algorithm.__name__ for algorithm in ALGORITHMS])))
        print("Valid renderers: {}".format("|".join(AVAILABLE_RENDERERS)))
        print("Rotations is an integer value measuring number of 90 degree clockwise rotations to perform")
        exit(1)
    renderer, renderer_name = renderer(AVAILABLE_RENDERERS, DEFAULT_RENDERER)
    pathfinding = True
    rows = int(args.all[0])
    columns = int(args.all[1])
    algorithm = get_algorithm()
    print("Algorithm: {}\nRows: {}\ncolumns: {}\nRenderer: {}".format(algorithm.__name__, rows, columns, renderer_name))

    valid_map = False
    while not valid_map:
        grid = ColoredGrid(rows, columns)
        grid = algorithm.on(grid)
        valid_map = renderer.is_valid(grid)     # type: ignore
        if not valid_map:
            print("Generated maze has no east/west linked ending cell. Recreating...")

    filename = strftime("%d%H%M%S", gmtime())

    renderer.render(grid, filename=filename)    # type: ignore

    print("Generated maze map has {} enemies".format(renderer.enemies_count))     # type: ignore

    grid = store_solution(grid)
    PNGRenderer.render(grid, coloring=True, filename=filename)
    if platform.system() == "Linux":
        subprocess.run(["xdg-open", "{}.png".format(filename)])
