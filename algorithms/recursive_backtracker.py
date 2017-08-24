from random import choice

from typing import Optional

from base.grid import Grid
from base.cell import Cell

"""
Recursive Backtracker algorithm picks a random starting cell and randomly walks. It cannot walk on an already visited
cell, and if finds at a dead-end (no more unvisited cells around current one), goes back in its steps until has a cell
at least one visited neighbor; then starts walking again.
"""


class RecursiveBacktracker:

    @staticmethod
    def on(grid: Grid, starting_cell: Optional[Cell] = None) -> Grid:
        if starting_cell is None:
            starting_cell = grid.random_cell()

        # We'll use the list as a stack to do very easily any backtracking
        walked_path = []
        walked_path.append(starting_cell)

        while len(walked_path) > 0:
            current_cell = walked_path[-1]
            unvisited_neighbors = [neighbor for neighbor in current_cell.neighbors if len(neighbor.links) == 0]

            if len(unvisited_neighbors) == 0:
                walked_path.pop()
            else:
                neighbor = choice(unvisited_neighbors)
                current_cell.link(neighbor)
                walked_path.append(neighbor)

        return grid
