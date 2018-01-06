from random import choice
from typing import TYPE_CHECKING

from algorithms.algorithm import AlgorithmWithLogging

if TYPE_CHECKING:  # Dont actually need Grid
    from base.grid import Grid


'''
A binary tree visits each cell in the grid and chooses to carve a passage either north or east with a simple random.
Causes topmost row and rightmost column to always be straight lines.
'''


class BinaryTree(AlgorithmWithLogging):

    def on(self, grid: Grid) -> None:
        self._prepareLogGrid(grid)

        for cell in grid.eachCell():
            self._logVisit(cell)

            neighbours = []
            if cell.north: neighbours.append(cell.north)
            if cell.east:  neighbours.append(cell.east)

            if len(neighbours) > 0:
                neighbour = choice(neighbours)
                cell += neighbour
                self._logLink(cell, neighbour)

            self.step()
