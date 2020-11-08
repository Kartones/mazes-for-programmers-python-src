from random import choice
from typing import Optional

from base.cell import Cell, is_cell
from base.grid import Grid
from algorithms.base_algorithm import Algorithm


class RecursiveBacktracker(Algorithm):
    """
    Recursive Backtracker algorithm picks a random starting cell and randomly walks.
    It cannot walk on an already visited cell, and if finds at a dead-end (no more unvisited cells around current one),
    goes back in its steps until has a cell at least one visited neighbor; then starts walking again.
    """

    def __init__(self, starting_cell: Optional[Cell] = None) -> None:
        self.starting_cell = starting_cell

    def on(self, grid: Grid) -> None:
        if self.starting_cell is None:
            self.starting_cell = grid.random_cell()
        if not is_cell(self.starting_cell) or self.starting_cell not in grid:
            ValueError("Starting point of the algorithm must be a valid cell in the grid")

        # We'll use the list as a stack to do very easily any backtracking
        walked_path = []
        walked_path.append(self.starting_cell)

        while walked_path:
            current_cell = walked_path[-1]

            unvisited_neighbors = [neighbor for neighbor in current_cell.neighbors if not neighbor.links]
            if not unvisited_neighbors:
                walked_path.pop()
            else:
                neighbor = choice(unvisited_neighbors)
                current_cell += neighbor
                walked_path.append(neighbor)
