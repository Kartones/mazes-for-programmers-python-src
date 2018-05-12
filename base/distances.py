from typing import Dict, List, Optional, Tuple, TYPE_CHECKING

# Avoid cyclic import, as Cell uses Distances
if TYPE_CHECKING:
    from base.cell import Cell  # noqa: F401
else:
    Cell = "Cell"


Cells = Dict[Cell, int]


class Distances:

    def __init__(self, root: Cell) -> None:
        if not is_cell(root):
            raise ValueError("Root must be a cell")

        self.root: Cell = root
        self._cells: Cells = dict()
        self._cells[root] = 0

    def __getitem__(self, cell: Cell) -> Optional[int]:
        if not is_cell(cell):
            raise IndexError("Distances must be indexed with a cell")

        if cell in self._cells.keys():
            return self._cells[cell]
        return None

    def __setitem__(self, cell: Cell, distance: int) -> None:
        if not is_cell(cell):
            raise IndexError("Distances must be indexed with a cell")

        self._cells[cell] = distance

    @property
    def cells(self) -> List[Cell]:
        return list(self._cells.keys())

    @property
    def max(self) -> Tuple[Cell, int]:
        max_distance = 0
        max_cell = self.root

        for cell in self._cells:
            if self._cells[cell] > max_distance:
                max_cell = cell
                max_distance = self._cells[cell]

        return max_cell, max_distance

    def path_to(self, destination: Cell) -> "Distances":
        """
        Traverses backwards, from destination to root/origin
        """
        if not is_cell(destination):
            raise ValueError("Destination must be a cell")

        current_cell = destination

        breadcrumbs = Distances(self.root)
        breadcrumbs[current_cell] = self._cells[current_cell]

        while current_cell != self.root:
            for neighbor in current_cell.links:
                if self._cells[neighbor] < self._cells[current_cell]:
                    breadcrumbs[neighbor] = self._cells[neighbor]
                    current_cell = neighbor
                    break

        return breadcrumbs


def is_cell(cell: Cell) -> bool:
    return type(cell).__name__ == Cell
