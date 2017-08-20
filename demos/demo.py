import sys
from typing import cast, Tuple, Type, Union     # noqa: F401

from base.grid import Grid
from base.distance_grid import DistanceGrid
from base.colored_grid import ColoredGrid

from algorithms.binary_tree import BinaryTree
from algorithms.sidewinder import Sidewinder

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

import renderers.ascii_renderer as ASCIIRenderer
import renderers.unicode_renderer as UNICODERenderer
import renderers.png_renderer as PNGRenderer

from utils.rotator import Rotator


ALGORITHMS = [BinaryTree, Sidewinder]
DEFAULT_RENDERER = "UNICODERenderer"
RENDERERS = [UNICODERenderer, ASCIIRenderer, PNGRenderer]


def validate_algoritm(command_line_argument: str) -> Type:
    for algorithm in ALGORITHMS:
        if algorithm.__name__ == command_line_argument:
            return algorithm
    raise ValueError("Invalid algorithm. Valid algorithms: {}".format("|".join(
        [algorithm.__name__ for algorithm in ALGORITHMS])))


def validate_renderer(command_line_argument: str) -> "Module":      # type: ignore
    for renderer in RENDERERS:
        if command_line_argument in globals():
            if globals()[command_line_argument] == renderer:
                return renderer
    raise ValueError("Invalid renderer. Valid renderers: {}".format("|".join(
        [renderer.__name__ for renderer in RENDERERS])))


def get_renderer() -> Tuple["Module", str]:     # type: ignore
    if len(sys.argv) > 4:
        try:
            renderer = validate_renderer(sys.argv[4])
            renderer_name = sys.argv[4]
        except ValueError as error:
            print(error)
            exit(1)
    else:
        renderer_name = DEFAULT_RENDERER
        renderer = globals()[DEFAULT_RENDERER]
    return renderer, renderer_name


def get_rotations() -> int:
    if len(sys.argv) > 5:
        rotations = int(sys.argv[5])
    else:
        rotations = 0
    return rotations


# see ALGORITHMS for list of types
def get_algorithm():    # type: ignore
    try:
        algorithm = validate_algoritm(sys.argv[3])
    except ValueError as error:
        print(error)
        exit(1)
    return algorithm


def get_pathfinding() -> bool:
    if len(sys.argv) > 6:
        return sys.argv[6] == "--pathfinding"
    else:
        return False


def get_coloring() -> bool:
    if len(sys.argv) > 7:
        return sys.argv[7] == "--coloring"
    else:
        return False


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:\nPYTHONPATH=. python3 demos/demo.py <rows> <columns> <algorithm> [renderer] [rotations]", end="")
        print(" [--pathfinding]")
        print("Valid algorithms: {}".format("|".join([algorithm.__name__ for algorithm in ALGORITHMS])))
        print("Valid renderers: {}".format("|".join([renderer.__name__ for renderer in RENDERERS])))
        print("Rotations is an integer value measuring number of 90 degree clockwise rotations to perform")
        print("Pathfinding flag shows distances between cells")
        exit(1)
    renderer, renderer_name = get_renderer()
    rotations = get_rotations()
    pathfinding = get_pathfinding()

    rows = int(sys.argv[1])
    columns = int(sys.argv[2])
    algorithm = get_algorithm()
    coloring = get_coloring()

    print("Algorithm: {}\nRows: {}\ncolumns: {}\nRenderer: {}".format(algorithm.__name__, rows, columns, renderer_name))
    print("90deg Rotations: {}\nPathfinding: {}\nColoring: {}".format(rotations, pathfinding, coloring))

    # here coloring takes precedence, because ColoredGrid inherits from DistanceGrid
    if coloring:
        grid = ColoredGrid(rows, columns)  # type: Union[Grid, DistanceGrid, ColoredGrid]
    elif pathfinding:
        grid = DistanceGrid(rows, columns)
    else:
        grid = Grid(rows, columns)

    grid = algorithm.on(grid)

    for num in range(rotations):
        grid = Rotator.on(grid)

    # here pathfinding first, so if also colored we'll see the route colored, else if colored will see all maze painted
    if pathfinding:
        start_row, start_column, end_row, end_column = LongestPath.calculate(cast(DistanceGrid, grid))
        print("Solving maze from row {} column {} to row {} column {}".format(
            start_row, start_column, end_row, end_column))
        grid = Dijkstra.calculate_distances(cast(DistanceGrid, grid), start_row, start_column, end_row, end_column)
    elif coloring:
        start_row = round(grid.rows / 2)
        start_column = round(grid.columns / 2)
        print("Drawing colored maze with start row {} column {}".format(start_row, start_column))
        start_cell = grid.get_cell(start_row, start_column)
        if start_cell is None:
            raise IndexError("Invalid start cell row {} column {}".format(start_row, start_column))
        grid.distances = start_cell.distances()     # type: ignore

    # TODO: refactor render parameters into either "options" or kwargs
    # TODO: Also do console_demo and png_demo to avoid options explosion
    if coloring:
        renderer.render(grid, coloring=True)
    else:
        renderer.render(grid)
