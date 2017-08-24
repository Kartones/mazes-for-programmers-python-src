import time

import args
from typing import cast, Union    # noqa: F401

from base.grid import Grid
from base.distance_grid import DistanceGrid

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath

from demos.demo_utils import ALGORITHMS, get_pathfinding


def get_tries() -> int:
    tries = 100
    for key in args.assignments:
        if key == "--tries":
            try:
                tries = int(args.assignments[key][0])
                if tries < 1:
                    raise ValueError()
            except ValueError:
                tries = 100
    return tries


if __name__ == "__main__":
    if len(args.all) < 2:
        print("Usage:\nPYTHONPATH=. python3 demos/image_demo.py <rows> <columns> [--tries=<num>] [--pathfinding]",
              end="")
        exit(1)

    rows = int(args.all[0])
    columns = int(args.all[1])
    size = rows * columns
    tries = get_tries()

    pathfinding = get_pathfinding()

    algorithm_averages = {}
    algorithm_benchmarks = {}
    pathfinding_benchmarks = {}

    print("Rows: {}\ncolumns: {}\nTotal cells: {}\nRuns per algorithm: {}".format(rows, columns, size, tries))
    print("Pathfinding: {}".format(pathfinding))
    for algorithm in ALGORITHMS:
        print("> running {}".format(algorithm.__name__))

        pathfinding_timings = []
        timings = []
        deadend_counts = []
        for _ in range(tries):
            if pathfinding:
                grid = DistanceGrid(rows, columns)  # type: Union[Grid, DistanceGrid]
            else:
                grid = Grid(rows, columns)

            time_start = time.perf_counter()
            grid = algorithm.on(grid)    # type: ignore
            time_end = time.perf_counter()

            deadend_counts.append(len(grid.deadends))
            timings.append(time_end - time_start)

            if pathfinding:
                time_start = time.perf_counter()
                start_row, start_column, end_row, end_column = LongestPath.calculate(cast(DistanceGrid, grid))
                grid = Dijkstra.calculate_distances(cast(DistanceGrid, grid), start_row, start_column, end_row,
                                                    end_column)
                time_end = time.perf_counter()
                pathfinding_timings.append(time_end - time_start)

        total_deadends = sum(deadend_counts)
        algorithm_averages[algorithm] = total_deadends / len(deadend_counts)
        timings = sorted(timings)
        algorithm_benchmarks[algorithm] = {
            "min": timings[0],
            "max": timings[-1],
            "average": sum(timings) / tries
        }
        if pathfinding:
            pathfinding_timings = sorted(pathfinding_timings)
        pathfinding_benchmarks[algorithm] = {
            "min": pathfinding_timings[0],
            "max": pathfinding_timings[-1],
            "average": sum(pathfinding_timings) / tries
        }

    sorted_averages = sorted(algorithm_averages.items(), key=lambda x: -x[1])
    print("\nAverage dead-ends (deadends/total-cells, sorted by % desc):")
    for algorithm, average in sorted_averages:
        percentage = average * 100.0 / size
        print(" {:>22}: {:03.0f}/{:03d} ({:.2f}%)".format(algorithm.__name__, average, size, percentage))

    sorted_benchmarks = sorted(algorithm_benchmarks.items(), key=lambda x: -x[1]["average"])
    print("\nGeneration speed benchmark (seconds, sorted by average desc):")
    for algorithm, benchmark in sorted_benchmarks:
        print(" {:>22}: avg: {:03.6f} min: {:03.6f} max: {:03.6f}".format(algorithm.__name__, benchmark["average"],
              benchmark["min"], benchmark["max"]))

    if pathfinding:
        sorted_pathfinding_benchmarks = sorted(pathfinding_benchmarks.items(), key=lambda x: -x[1]["average"])
        print("\nPathfinding speed benchmark (seconds, sorted by average desc):")
        for algorithm, benchmark in sorted_pathfinding_benchmarks:
            print(" {:>22}: avg: {:03.6f} min: {:03.6f} max: {:03.6f}".format(algorithm.__name__, benchmark["average"],
                  benchmark["min"], benchmark["max"]))
