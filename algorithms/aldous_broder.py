from algorithms.base_algorithm import Algorithm
from base.grid import Grid


class AldousBroder(Algorithm):
    """
    Aldous-Broder algorithm works by always choosing a random neighbor of a randomly-selected also cell, and linking
    them if not yet visited ("random walking"), repeating until all cells are visited once.
    Can take long to compute on big grids (slow-to-finish).
    """

    def on(self, grid: Grid) -> None:
        current_cell = grid.random_cell()
        unvisited_count = grid.size - 1

        while unvisited_count > 0:
            neighbor = current_cell.random_neighbour()
            if neighbor is None:
                raise ValueError("Aldous-Broder algorithm needs all cells to have at least one neighbor")
            if len(neighbor.links) == 0:
                current_cell += neighbor
                unvisited_count -= 1
            current_cell = neighbor
