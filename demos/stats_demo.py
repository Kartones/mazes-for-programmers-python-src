import args

from base.grid import Grid

from demos.demo_utils import ALGORITHMS

# TODO: Add pathfinding
# TODO: Add time run metrics

if __name__ == "__main__":
    if len(args.all) < 2:
        print("Usage:\nPYTHONPATH=. python3 demos/image_demo.py <rows> <columns> [--pathfinding]", end="")
        exit(1)

    rows = int(args.all[0])
    columns = int(args.all[1])
    size = rows * columns
    tries = 100

    averages = {}

    print("Rows: {}\ncolumns: {}\nRuns per algorithm: {}".format(rows, columns, tries))
    for algorithm in ALGORITHMS:
        print("> running {}".format(algorithm.__name__))

        deadend_counts = []
        for _ in range(tries):
            grid = Grid(rows, columns)
            grid = algorithm.on(grid)    # type: ignore
            deadend_counts.append(len(grid.deadends))

        total_deadends = sum(deadend_counts)
        averages[algorithm] = total_deadends / len(deadend_counts)

    sorted_averages = sorted(averages.items(), key=lambda x: -x[1])

    print("\nAverage dead-ends per {}x{} maze ({} cells):".format(rows, columns, size))
    for algorithm, average in sorted_averages:
        percentage = average * 100.0 / size
        print(" {:>16}: {:.0f}/{:02d} ({:.2f}%)".format(algorithm.__name__, average, size, percentage))
