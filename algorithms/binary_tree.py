from random import choice

from algorithms.base_algorithm import Algorithm
from base.grid import Grid


class BinaryTree(Algorithm):
    """
    A binary tree visits each cell in the grid and chooses to carve a passage either north or east with a simple random.
    Causes topmost row and rightmost column to always be straight lines.
    """

    def on(self, grid: Grid) -> None:
        for cell in grid.each_cell():
            neighbors = []
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)
            if len(neighbors) > 0:
                neighbor = choice(neighbors)
                cell += neighbor
