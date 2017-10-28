from typing import Dict, List, Optional, Tuple, TYPE_CHECKING   # noqa: F401

# Avoid cyclic import, as Cell uses Distances
if TYPE_CHECKING:
    from base.cell import Cell  # noqa: F401


class Distances:

    def __init__(self, root: "Cell") -> None:
        self.root = root
        self._cells = dict()         # type: Dict[Cell, int]
        self._cells[root] = 0

    def __getitem__(self, cell: "Cell") -> Optional[int]:
        try:
            return self._cells[cell]
        except KeyError:
            return None

    def __setitem__(self, cell: "Cell", distance: int) -> None:
        self._cells[cell] = distance

    @property
    def cells(self) -> List["Cell"]:
        return list(self._cells.keys())

    @property
    def max(self) -> Tuple["Cell", int]:
        max_distance = 0
        max_cell = self.root

        for cell in self._cells:
            if self._cells[cell] > max_distance:
                max_cell = cell
                max_distance = self._cells[cell]

        return max_cell, max_distance

    def path_to(self, destination: "Cell") -> "Distances":
        """
        Traverses backwards, from destination to root/origin
        """
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
