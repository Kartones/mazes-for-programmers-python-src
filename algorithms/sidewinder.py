from random import choice, randint

from algorithms.base_algorithm import Algorithm
from base.grid import Grid


class Sidewinder(Algorithm):
    """
    A sidewinder visits each cell in the grid and chooses to carve a passage either north or east
    (similar to Binary Tree), but running row by row.
    Causes topmost row to always be a straight line.
    """

    def on(self, grid: Grid) -> None:
        for row in grid.each_row():
            run = []
            for cell in row:

                run.append(cell)
                at_eastern_boundary = cell.east is None
                at_northen_boundary = cell.north is None
                should_close_out = at_eastern_boundary or (not at_northen_boundary and randint(0, 1) == 0)
                if should_close_out:
                    member = choice(run)
                    if member.north:
                        member += member.north
                    run.clear()
                else:
                    cell += cell.east
