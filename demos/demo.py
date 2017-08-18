import sys
from typing import cast, Tuple, Type, Union     # noqa: F401

from base.grid import Grid
from base.distance_grid import DistanceGrid

from algorithms.binary_tree import BinaryTree
from algorithms.sidewinder import Sidewinder

import pathfinders.dijkstra as Dijkstra

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

    print("Algorithm: {}\nRows: {}\ncolumns: {}\nRenderer: {}".format(algorithm.__name__, rows, columns, renderer_name))
    print("90deg Rotations: {}\nPathfinding: {}".format(rotations, pathfinding))

    if pathfinding:
        grid = DistanceGrid(rows, columns)  # type: Union[Grid, DistanceGrid]
    else:
        grid = Grid(rows, columns)

    grid = algorithm.on(grid)

    for num in range(rotations):
        grid = Rotator.on(grid)

    if pathfinding:
        grid = Dijkstra.calculate_distances(cast(DistanceGrid, grid), 0, 0)

    renderer.render(grid)
