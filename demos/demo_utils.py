import args
from typing import List, Tuple, Type

from algorithms.binary_tree import BinaryTree
from algorithms.sidewinder import Sidewinder
from algorithms.aldous_broder import AldousBroder
from algorithms.wilson import Wilson
from algorithms.hunt_and_kill import HuntAndKill

import renderers.ascii_renderer as ASCIIRenderer
import renderers.unicode_renderer as UNICODERenderer
import renderers.png_renderer as PNGRenderer

ALGORITHMS = [AldousBroder, BinaryTree, HuntAndKill, Sidewinder, Wilson]
ALL_RENDERERS = [UNICODERenderer, ASCIIRenderer, PNGRenderer]


def validate_algorithm(desired_algorithm: str) -> Type:
    for algorithm in ALGORITHMS:
        if algorithm.__name__ == desired_algorithm:
            return algorithm
    raise ValueError("Invalid algorithm. Valid algorithms: {}".format("|".join(
        [algorithm.__name__ for algorithm in ALGORITHMS])))


def get_renderer(available_renderers: List[str], default_renderer: str) -> Tuple["Module", str]:     # type: ignore
    renderer_name = default_renderer
    renderer = globals()[default_renderer]
    for key in args.assignments:
        if key == "--renderer":
            try:
                renderer_name = args.assignments[key][0]
                if renderer_name in available_renderers and renderer_name in globals():
                    renderer = globals()[renderer_name]
            except ValueError as error:
                print(error)
                exit(1)
    return renderer, renderer_name


def get_rotations() -> int:
    rotations = 0
    for key in args.assignments:
        if key == "--rotations":
            try:
                rotations = int(args.assignments[key][0])
            except ValueError:
                rotations = 0
    return rotations


# see ALGORITHMS for list of types
def get_algorithm():    # type: ignore
    try:
        algorithm = validate_algorithm(args.all[2])
    except ValueError as error:
        print(error)
        exit(1)
    return algorithm


def get_pathfinding() -> bool:
    return bool("--pathfinding" in args.flags)
