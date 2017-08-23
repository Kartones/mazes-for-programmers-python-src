from random import choice

from base.grid import Grid

"""
Aldous-Broder algorithm works by always choosing a random neighbor of a randomly-selected also cell, and linking them
if not yet visited ("random walking"), repeating until all cells are visited once.
Can take long to compute on big grids (slow-to-finish).
"""


class AldousBroder:

    @staticmethod
    def on(grid: Grid) -> Grid:
        current_cell = grid.random_cell()
        unvisited_count = grid.size - 1

        while unvisited_count > 0:
            neighbor = choice(current_cell.neighbors)
            if neighbor is None:
                raise ValueError("Aldous-Broder algorithm needs all cells to have at least one neighbor")
            if len(neighbor.links) == 0:
                current_cell.link(neighbor)
                unvisited_count -= 1
            current_cell = neighbor

        return grid
