from random import choice

from base.grid import Grid

"""
A binary tree visits each cell in the grid and chooses to carve a passage either north or east with a simple random.
Causes topmost row and rightmost column to always be straight lines.
"""


class BinaryTree:

    @staticmethod
    def on(grid: Grid) -> Grid:
        for cell in grid.each_cell():
            neighbors = []
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)
            if len(neighbors) > 0:
                cell.link(choice(neighbors))
        return grid
