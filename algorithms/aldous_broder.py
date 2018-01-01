from random import choice
from typing import TYPE_CHECKING

from algorithms.algorithm import AlgorithmWithLogging
from base.grid import Grid


'''
Aldous-Broder algorithm works by always choosing a random neighbor of a randomly-selected cell, and linking them
if not yet visited ('random walking'). Repeat until all cells are visited once.
Can take long to compute on big grids (slow-to-finish).
'''


class AldousBroder(AlgorithmWithLogging):
    
    def on(self, grid: Grid) -> Grid:
        self._prepareLogGrid(grid)
        
        cell = grid.randomCell()
        set_count = 0

        while set_count < grid.size-1:
            self._logVisit(cell)
            neighbour = cell.randomNeighbour()

            message = 'Aldous-Broder algorithm needs all cells to have at least one neighbour'
            assert neighbour is not None, message

            if neighbour.nl == 0:
                cell += neighbour
                self._logLink(cell, neighbour)
                set_count += 1
            cell = neighbour

            self.step()
