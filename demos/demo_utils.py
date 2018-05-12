from argparse import ArgumentTypeError
from typing import List, Type

from algorithms.base_algorithm import Algorithm
from algorithms.aldous_broder import AldousBroder
from algorithms.binary_tree import BinaryTree
from algorithms.hunt_and_kill import HuntAndKill
from algorithms.recursive_backtracker import RecursiveBacktracker
from algorithms.sidewinder import Sidewinder
from algorithms.wilson import Wilson
from exporters.base_exporter import Exporter
from exporters.ascii_exporter import ASCIIExporter
from exporters.png_exporter import PNGExporter
from exporters.unicode_exporter import UnicodeExporter
from exporters.wolf3d_exporter import Wolf3DExporter


ALGORITHMS: List[Type[Algorithm]] = [AldousBroder, BinaryTree, HuntAndKill, RecursiveBacktracker, Sidewinder, Wilson]
ALGORITHM_NAMES: List[str] = [x.__name__ for x in ALGORITHMS]
# TODO: Add PixelExporter
EXPORTERS: List[Type[Exporter]] = [Wolf3DExporter, PNGExporter, UnicodeExporter, ASCIIExporter]
EXPORTER_NAMES: List[str] = [x.__name__ for x in EXPORTERS]


def _instantiate_algorithm(desired_algorithm: str) -> Algorithm:
    for algorithm in ALGORITHMS:
        if algorithm.__name__ == desired_algorithm:
            return algorithm()

    raise ValueError("Invalid algorithm. Valid algorithms: {}".format("|".join(
        [algorithm.__name__ for algorithm in ALGORITHMS])))


def get_algorithm(algorithm: str, available_algorithms: List[str]) -> Algorithm:
    if algorithm in available_algorithms:
        return _instantiate_algorithm(algorithm)

    raise ValueError("Invalid algorithm. Available algorithms: {}".format("|".join(available_algorithms)))


def _instantiate_exporter(desired_exporter: str) -> Exporter:
    for exporter in EXPORTERS:
        if exporter.__name__ == desired_exporter:
            return exporter()

    raise ValueError("Invalid exporter. Valid exporters: {}".format("|".join(
        [exporter.__name__ for exporter in EXPORTERS])))


def get_exporter(exporter: str, available_exporters: List[str]) -> Exporter:
    if exporter in available_exporters:
        return _instantiate_exporter(exporter)

    raise ValueError("Invalid exporter. Available exporters: {}".format("|".join(available_exporters)))


def str2bool(source_string: str) -> bool:
    # https://stackoverflow.com/a/43357954/2531987
    if source_string.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif source_string.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise ArgumentTypeError("Stringified boolean value expected")
