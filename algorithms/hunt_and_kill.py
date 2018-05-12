from random import choice
from typing import cast, Optional

from algorithms.base_algorithm import Algorithm

from base.grid import Grid
from base.cell import Cell


class HuntAndKill(Algorithm):
    """
    Hunt-and-Kill algorithm picks a random starting cell and randomly walks. It cannot walk on an already visited cell,
    and if finds at a dead-end (no more unvisited cells around current one), "hunts" from the northwest corner the
    first cell that is unvisted and has at least one visited neighbor; then starts walking again.
    """

    def on(self, grid: Grid) -> None:
        current_cell: Optional[Cell] = grid.random_cell()

        while current_cell is not None:
            current_cell = cast(Cell, current_cell)  # Mypy doesn't detects while condition

            unvisited_neighbors = [neighbor for neighbor in current_cell.neighbors if len(neighbor.links) == 0]
            if len(unvisited_neighbors) > 0:
                # as long as there are unvisited paths, walk them
                neighbor = choice(unvisited_neighbors)
                current_cell += neighbor
                current_cell = neighbor
            else:
                # enter hunt mode, find first unvisited cell near any visited cell
                current_cell = None

                for cell in grid.each_cell():
                    visited_neighbors = [neighbor for neighbor in cell.neighbors if len(neighbor.links) > 0]
                    if len(cell.links) == 0 and len(visited_neighbors) > 0:
                        current_cell = cast(Cell, cell)  # outside of Mypy it's a mere assignment
                        neighbor = choice(visited_neighbors)
                        current_cell += neighbor
                        break
