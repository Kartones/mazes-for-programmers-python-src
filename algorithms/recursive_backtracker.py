from random import choice
from typing import TYPE_CHECKING, Optional

from algorithms.algorithm import AlgorithmWithLogging
from base.cell import isCell

if TYPE_CHECKING:
    from base.cell import Cell
    from base.grid import Grid


'''
Recursive Backtracker algorithm picks a random starting cell and randomly walks. It cannot walk on an already visited
cell, and if finds at a dead-end (no more unvisited cells around current one), goes back in its steps until has a cell
at least one visited neighbor; then starts walking again.
'''


class RecursiveBacktracker(AlgorithmWithLogging):

    def __init__(self, log: bool = True, start: Optional[Cell] = None) -> None:
        super().__init__(log=log)
        self.start = start

    def on(self, grid: Grid) -> None:
        if self.start is None:
            start = grid.randomCell()
        elif isCell(start) and start in grid:
            start = start
        else:
            ValueError('The starting point of the algorithm must be a cell in the grid')

        # We'll use the list as a stack to do any backtracking
        walked_path = []
        walked_path.append(start)

        while len(walked_path) > 0:
            current_cell = walked_path[-1]
            unvisited_neighbours = [n for n in current_cell.neighbours if n.nLinks == 0]

            if len(unvisited_neighbours) == 0:
                walked_path.pop()
            else:
                neighbour = choice(unvisited_neighbours)
                current_cell += neighbour
                walked_path.append(neighbour)
            self.step()
