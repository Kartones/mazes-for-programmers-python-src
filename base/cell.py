from random import choice
from typing import Any, cast, Dict, Hashable, List, Optional
import warnings

from base.distances import Distances

Links = Dict["Cell", bool]
CellList = List["Cell"]


class Cell:

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def links(self) -> CellList:
        return list(self._links.keys())

    @property
    def neighbors(self) -> CellList:
        neighbors_list: CellList = []
        if self.north:
            neighbors_list.append(self.north)
        if self.south:
            neighbors_list.append(self.south)
        if self.east:
            neighbors_list.append(self.east)
        if self.west:
            neighbors_list.append(self.west)
        return neighbors_list

    @property
    def distances(self) -> Distances:
        distances = Distances(self)
        frontier = [self]

        while len(frontier) > 0:
            new_frontier = []
            for cell in frontier:
                for linked_cell in cell.links:
                    if distances[linked_cell] is None and distances[cell] is not None:
                        distances[linked_cell] = cast(int, distances[cell]) + 1
                        new_frontier.append(linked_cell)
            frontier = new_frontier

        return distances

    @property
    def data(self) -> Dict:
        return self._data

    def __init__(self, row: int, column: int) -> None:
        if row is None or row < 0:
            raise ValueError("Row must be a positive integer")
        if column is None or column < 0:
            raise ValueError("Column must be a positive integer")

        self._row: int = row
        self._column: int = column
        self._links: Dict[Cell, bool] = {}
        self._data: Dict = {}
        self.north: Optional[Cell] = None
        self.south: Optional[Cell] = None
        self.east: Optional[Cell] = None
        self.west: Optional[Cell] = None

    def link(self, cell: "Cell", bidirectional: bool = True) -> "Cell":
        """
        Links current cell to specified one
        """
        if not self._is_cell(cell):
            raise ValueError("Link can only be made between two cells")

        self._links[cell] = True
        if bidirectional:
            cell.link(cell=self, bidirectional=False)
        return self

    def unlink(self, cell: "Cell", bidirectional: bool = True) -> "Cell":
        """
        Unlinks current cell from specified one
        """
        if cell is None:
            warnings.warn("Attempted to remove non-existant link", UserWarning)
        elif not self._is_cell(cell):
            raise ValueError("Link can only be removed between two cells")

        if self.linked_to(cell):
            del self._links[cell]
            if bidirectional:
                cell.unlink(cell=self, bidirectional=False)
        return self

    # TODO: this was previously not doing integrity checks. see if worth to make it again restrictive
    def linked_to(self, cell: Optional["Cell"]) -> bool:
        if self._is_cell(cell):
            return cell in self._links
        elif cell is None:
            return False
        else:
            raise ValueError("Attempted to check link with non-cell")

    def random_neighbour(self) -> Optional["Cell"]:
        if len(self.neighbors) == 0:
            return None
        else:
            return choice(self.neighbors)

    def has_data(self, key: Hashable) -> bool:
        return key in self.data.keys()

    @staticmethod
    def _is_cell(cell: Any) -> bool:
        return isinstance(cell, Cell)

    def __iadd__(self, cell: "Cell") -> "Cell":
        """
        Overload for the += operator with the link method
        """
        self.link(cell)
        return self

    def __isub__(self, cell: "Cell") -> "Cell":
        """
        Overload for the -= operator with the link method
        """
        self.unlink(cell)
        return self

    def __and__(self, other_cell: Optional["Cell"]) -> bool:
        """
        Overload for the & operator with the linked? method
        """
        return self.linked_to(other_cell)

    def __hash__(self) -> int:
        return hash((self.column, self.row))

    def __repr__(self) -> str:
        return "({},{}) = {}".format(self.column, self.row, str(hex(id(self))))

    # Note: The following methods actually don't take into account neighbors/linked-cells, but for now is enough

    def __eq__(self, other_cell: "Cell") -> bool:       # type: ignore
        return self.row == other_cell.row and self.column == other_cell.column

    def __ne__(self, other_cell: "Cell") -> bool:       # type: ignore
        return not self == other_cell
