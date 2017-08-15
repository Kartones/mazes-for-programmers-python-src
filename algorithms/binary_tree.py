from random import choice

from typing import List, Union  # noqa: F401

from base.cell import Cell   # noqa: F401
from base.grid import Grid

"""
A binary tree visits each cell in the grid and chooses to carve a passage either north or east.
"""


class BinaryTree:

    @staticmethod
    def on(grid: Grid) -> Grid:
        for cell in grid.each_cell():
            neighbors = []         # type: List[Union[None, Cell]]
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)
            if len(neighbors) > 0:
                cell.link(choice(neighbors))
        return grid
