import sys
from typing import Type

from base.grid import Grid

from algorithms.binary_tree import BinaryTree
from algorithms.sidewinder import Sidewinder

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


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:\nPYTHONPATH=. python3 demos/demo.py <rows> <columns> <algorithm> [renderer] [rotations]")
        print("Valid algorithms: {}".format("|".join([algorithm.__name__ for algorithm in ALGORITHMS])))
        print("Valid renderers: {}".format("|".join([renderer.__name__ for renderer in RENDERERS])))
        print("Rotations is an integer value measuring number of 90 degree clockwise rotations to perform")
        exit(1)
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
    if len(sys.argv) > 5:
        rotations = int(sys.argv[5])
    else:
        rotations = 0

    rows = int(sys.argv[1])
    columns = int(sys.argv[2])
    try:
        algorithm = validate_algoritm(sys.argv[3])
    except ValueError as error:
        print(error)
        exit(1)

    print("Algorithm: {}\nRows: {}\ncolumns: {}\nRenderer: {}".format(algorithm.__name__, rows, columns, renderer_name))
    print("90deg Rotations: {}".format(rotations))

    grid = Grid(rows, columns)
    grid = algorithm.on(grid)

    for num in range(rotations):
        grid = Rotator.on(grid)

    renderer.render(grid)
