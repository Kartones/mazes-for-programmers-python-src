# Temporarilly add parent folder to path (if not already added)
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import argparse
import time
from typing import Union, cast  # noqa: F401

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath
from base.distance_grid import DistanceGrid
from base.grid import Grid
from demos.demo_utils import ALGORITHMS, str2bool

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run statistics for all algorithms')
    parser.add_argument('rows', type=int, help='number or rows')
    parser.add_argument('cols', type=int, help='number or columns')
    parser.add_argument('-t', '--tries', type=int, default=100, help='number of tries')
    parser.add_argument('-p', '--pathfinding', type=str2bool, default=False, help='whether to find the path through the maze')
    args = parser.parse_args()

    rows = args.rows
    columns = args.cols
    size = rows * columns
    tries = args.tries
    pathfinding = args.pathfinding

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
