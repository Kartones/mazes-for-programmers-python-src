from typing import cast, Dict, List, Optional    # noqa: F401

from base.distances import Distances


class Cell:

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def links(self) -> List["Cell"]:
        return list(self._links.keys())

    @property
    def neighbors(self) -> List["Cell"]:
        neighbors_list = []         # type: List[Cell]
        if self.north:
            neighbors_list.append(self.north)
        if self.south:
            neighbors_list.append(self.south)
        if self.east:
            neighbors_list.append(self.east)
        if self.west:
            neighbors_list.append(self.west)
        return neighbors_list

    def __init__(self, row: int, column: int) -> None:
        if row is None or row < 0:
            raise ValueError("Row must be a positive integer")
        if column is None or column < 0:
            raise ValueError("Column must be a positive integer")

        self._row = row         # type: int
        self._column = column   # type: int
        self._links = {}        # type: Dict[Cell, bool]
        self.north = None       # type: Optional[Cell]
        self.south = None       # type: Optional[Cell]
        self.east = None        # type: Optional[Cell]
        self.west = None        # type: Optional[Cell]

    def link(self, cell: "Cell", bidirectional: bool = True) -> "Cell":
        self._links[cell] = True
        if bidirectional:
            cell.link(self, False)
        return self

    def unlink(self, cell: "Cell", bidirectional: bool = True) -> "Cell":
        del self._links[cell]
        if bidirectional:
            cell.unlink(self, False)
        return self

    def linked_to(self, cell: "Cell") -> bool:
        return cell in self._links

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

    # The following methods actually lie because don't take into account neighbors/linked-cells, but for now is enough

    def __hash__(self) -> int:
        return hash((self.column, self.row))

    def __repr__(self) -> str:
        return "({},{})".format(self.column, self.row)

    def __eq__(self, other_cell: "Cell") -> bool:       # type: ignore
        return self.row == other_cell.row and self.column == other_cell.column

    def __ne__(self, other_cell: "Cell") -> bool:       # type: ignore
        return not self == other_cell
