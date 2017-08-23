from random import choice

from typing import cast, Optional     # noqa: F401

from base.grid import Grid
from base.cell import Cell      # noqa: F401

"""
Hunt-and-Kill algorithm picks a random starting cell and randomly walks. It cannot walk on an already visited cell, and
if finds at a dead-end (no more unvisited cells around current one), "hunts" from the northwest corner the first cell
that is unvisted and has at least one visited neighbor; then starts walking again.
"""


class HuntAndKill:

    @staticmethod
    def on(grid: Grid) -> Grid:
        current_cell = grid.random_cell()  # type: Optional[Cell]

        while current_cell is not None:
            unvisited_neighbors = \
                [neighbor for neighbor in current_cell.neighbors if len(neighbor.links) == 0]

            if len(unvisited_neighbors) > 0:
                # as long as there are unvisited paths, walk them
                neighbor = choice(unvisited_neighbors)
                current_cell.link(neighbor)
                current_cell = neighbor
            else:
                # enter hunt mode, find first unvisited cell near any visited cell
                current_cell = None
                for cell in grid.each_cell():
                    visited_neighbors = [neighbor for neighbor in cell.neighbors if len(neighbor.links) > 0]
                    if len(cell.links) == 0 and len(visited_neighbors) > 0:
                        current_cell = cast(Cell, cell)
                        neighbor = choice(visited_neighbors)
                        current_cell.link(neighbor)
                        break

        return grid
