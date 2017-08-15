#!/usr/bin/env python3

from typing import Dict, List, Optional, Union    # noqa: F401


class Cell:

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def links(self) -> List:
        return list(self._links.keys())

    def __init__(self, row: int, column: int) -> None:
        if row is None or row < 0:
            raise ValueError("Row must be a positive integer")
        if column is None or column < 0:
            raise ValueError("Column must be a positive integer")

        self._row = row         # type: int
        self._column = column   # type: int
        self._links = {}        # type: Dict
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

    def neighbors(self) -> List[Union[None, "Cell"]]:
        neighbors_list = []         # type: List[Union[None, Cell]]
        if self.north:
            neighbors_list.append(self.north)
        if self.south:
            neighbors_list.append(self.south)
        if self.east:
            neighbors_list.append(self.east)
        if self.west:
            neighbors_list.append(self.west)
        return neighbors_list

    def __hash__(self) -> int:
        return hash((self.column, self.row))

    def __repr__(self) -> str:
        return "({},{})".format(self.column, self.row)

    def __eq__(self, other_cell: "Cell") -> bool:       # type: ignore
        return self.row == other_cell.row and self.column == other_cell.column

    def __ne__(self, other_cell: "Cell") -> bool:       # type: ignore
        return not self == other_cell
