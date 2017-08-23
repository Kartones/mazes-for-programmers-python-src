from random import choice

from base.grid import Grid
from base.cell import Cell      # noqa: F401

"""
Wilson algorithm works by choosing a random cell as origin, another as destination, and performs as loop-erased
random walk towards it using the neighbors. Stores the path until comes to either destination or a "walked" path cell,
former causing the algorithm to delete the loop until there and keep going.
Takes a long to compute on big grids (slow-to-start).
"""


class Wilson:

    @staticmethod
    def on(grid: Grid) -> Grid:
        unvisited = []  # Type: List[Cell]
        for cell in grid.each_cell():
            unvisited.append(cell)

        first_cell = choice(unvisited)
        del unvisited[unvisited.index(first_cell)]

        while len(unvisited) > 0:
            # start a walk
            cell = choice(unvisited)
            path = [cell]

            while cell in unvisited:
                cell = choice(cell.neighbors)
                try:
                    position = path.index(cell)
                    # already walked, perform loop-erase
                    path = path[:position + 1]
                except ValueError:
                    path.append(cell)

            # Passage carving once has found a valid path
            for index in range(len(path) - 1):
                path[index].link(path[index + 1])
                del unvisited[unvisited.index(path[index])]

        return grid
