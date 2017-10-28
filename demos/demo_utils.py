import args
from typing import List, Tuple, Type

from algorithms.binary_tree import BinaryTree
from algorithms.sidewinder import Sidewinder
from algorithms.aldous_broder import AldousBroder
from algorithms.wilson import Wilson
from algorithms.hunt_and_kill import HuntAndKill
from algorithms.recursive_backtracker import RecursiveBacktracker

from exporters.png_exporter import PNGExporter
from exporters.wolf3d_exporter import Wolf3DExporter
from exporters.unicode_exporter import UnicodeExporter
from exporters.ascii_exporter import ASCIIExporter


ALGORITHMS = [AldousBroder, BinaryTree, HuntAndKill, RecursiveBacktracker, Sidewinder, Wilson]
ALL_EXPORTERS = [Wolf3DExporter, PNGExporter, UnicodeExporter, ASCIIExporter]


def validate_algorithm(desired_algorithm: str) -> Type:
    for algorithm in ALGORITHMS:
        if algorithm.__name__ == desired_algorithm:
            return algorithm
    raise ValueError("Invalid algorithm. Valid algorithms: {}".format("|".join(
        [algorithm.__name__ for algorithm in ALGORITHMS])))


def get_exporter(available_exporters: List[str], default_exporter: str) -> Tuple["Module", str]:     # type: ignore
    exporter_name = default_exporter
    exporter = globals()[default_exporter]
    for key in args.assignments:
        if key == "--exporter":
            try:
                exporter_name = args.assignments[key][0]
                # Hacky but only method I know to get an alias of an imported module
                if exporter_name in available_exporters and exporter_name in globals():
                    exporter = globals()[exporter_name]
            except ValueError as error:
                print(error)
                exit(1)
    return exporter(), exporter_name


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
        return algorithm
    except ValueError as error:
        print(error)
        exit(1)


def get_pathfinding() -> bool:
    return bool("--pathfinding" in args.flags)
