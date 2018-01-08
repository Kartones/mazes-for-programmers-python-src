from random import choice
from typing import TYPE_CHECKING, Optional  # noqa: F401

from algorithms.algorithm import AlgorithmWithLogging

if TYPE_CHECKING:  # Dont actually need Grid
    from base.grid import Grid
    from base.cell import Cell  # noqa: F401
else:
    Grid = 'Grid'
    Cell = 'Cell'


'''
Hunt-and-Kill algorithm picks a random starting cell and randomly walks. It cannot walk on an already visited cell, and
if finds at a dead-end (no more unvisited cells around current one), 'hunts' from the northwest corner the first cell
that is unvisted and has at least one visited neighbour; then starts walking again.
'''


class HuntAndKill(AlgorithmWithLogging):

    def on(self, grid: Grid) -> None:
        self._prepareLogGrid(grid)

        cell = grid.randomCell()  # type: Optional[Cell]

        while cell is not None:
            self._logVisit(cell)
            unvisited = [n for n in cell.neighbours if n.nLinks == 0]

            if len(unvisited) > 0:
                # as long as there are unvisited paths, walk them
                neighbour = choice(unvisited)
                cell += neighbour
                self._logLink(cell, neighbour)
                cell = neighbour
            else:
                # enter hunt mode, find first unvisited cell near any visited cell
                cell = None
                self.step()

                for c in grid.eachCell():
                    self._logVisit(c)
                    visited = [n for n in c.neighbours if n.nLinks > 0]  # visited neighbours

                    if c.nLinks == 0 and len(visited) > 0:
                        cell = c
                        neighbour = choice(visited)
                        cell += neighbour
                        self._logLink(cell, neighbour)
                        break  # from the 'for' loop
                    self.step()

            self.step()
