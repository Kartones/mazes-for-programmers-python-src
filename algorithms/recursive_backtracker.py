from random import choice
from typing import TYPE_CHECKING, Optional

from algorithms.algorithm import Algorithm
from base.cell import Cell
from base.grid import Grid


'''
Recursive Backtracker algorithm picks a random starting cell and randomly walks. It cannot walk on an already visited
cell, and if finds at a dead-end (no more unvisited cells around current one), goes back in its steps until has a cell
at least one visited neighbor; then starts walking again.
'''


class RecursiveBacktracker(Algorithm):

    def on(self, grid: Grid, start: Optional[Cell] = None) -> None:
        if start is None:
            start = grid.randomCell()

        # We'll use the list as a stack to do any backtracking
        walked_path = []
        walked_path.append(start)

        while len(walked_path) > 0:
            current_cell = walked_path[-1]
            unvisited_neighbours = [n for n in current_cell.neighbours if n.nl == 0]

            if len(unvisited_neighbours) == 0:
                walked_path.pop()
            else:
                neighbour = choice(unvisited_neighbours)
                current_cell += neighbour
                walked_path.append(neighbour)
            self.step()
