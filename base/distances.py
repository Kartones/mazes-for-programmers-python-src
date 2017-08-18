from typing import Dict, List, Optional, TYPE_CHECKING   # noqa: F401

# Avoid cyclic import, as Cell uses Distances
if TYPE_CHECKING:
    from base.cell import Cell  # noqa: F401


class Distances:

    def __init__(self, root: "Cell") -> None:
        self.root = root
        self._cells = {}         # type: Dict[Cell, int]
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
