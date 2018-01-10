from random import choice
from typing import TYPE_CHECKING

from algorithms.algorithm import Algorithm

if TYPE_CHECKING:
    from base.grid import Grid
else:
    Grid = 'Grid'

'''
Wilson algorithm works by choosing a random cell as origin, another as destination, and performs as loop-erased
random walk towards it using the neighbors. Stores the path until comes to either destination or a 'walked' path cell,
former causing the algorithm to delete the loop until there and keep going.
Takes a long to compute on big grids (slow-to-start).
'''


class Wilson(Algorithm):

    def on(self, grid: Grid) -> None:
        unvisited = []
        for cell in grid.eachCell():
            unvisited.append(cell)

        first_cell = choice(unvisited)
        unvisited.remove(first_cell)

        while len(unvisited) > 0:
            # start a walk
            cell = choice(unvisited)
            path = [cell]

            while cell in unvisited:
                cell = cell.randomNeighbour()  # type: ignore
                try:
                    position = path.index(cell)
                    # already walked, perform loop-erase. e.g. 'A -> B -> C -> D -> B' becomes 'A -> B'
                    path = path[:position + 1]
                except ValueError:
                    path.append(cell)
                self.step()

            # Passage carving once has found a valid path
            for index in range(len(path) - 1):
                path[index] += (path[index + 1])
                unvisited.remove(path[index])
                self.step()
