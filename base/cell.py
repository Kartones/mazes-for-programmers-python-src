from random import choice
from typing import Dict, List, Optional, Tuple, cast  # noqa: F401

from base.distances import Distances


class Cell:

    @property
    def links(self):
        return self._links

    @links.getter
    def links(self):
        return list(self._links.keys())

    @property
    def neighbours(self) -> List['Cell']:
        ''' List of neighbours '''
        neighbours = []         # type: List[Cell]
        if self.north: neighbours.append(self.north)
        if self.south: neighbours.append(self.south)
        if self.east:  neighbours.append(self.east)
        if self.west:  neighbours.append(self.west)
        return neighbours
    
    def randomNeighbour(self) -> Optional['Cell']:
        ''' Return a random neighbour '''
        if self.nn > 0: return choice(self.neighbours)
    
    @property
    def nl(self) -> int:
        ''' Number of links '''
        return len(self.links)
    
    @property
    def nn(self) -> int:
        ''' Number of neighbours '''
        return len(self.neighbours)

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

    def __init__(self, row: int, col: int) -> None:
        if row is None or row < 0:
            raise ValueError("Row must be a positive integer")
        if col is None or col < 0:
            raise ValueError("Column must be a positive integer")

        self.row = row          # type: int
        self.col = col          # type: int
        self._links = {}        # type: Dict[Cell, bool]
        self._data = {}         # type: Dict
        self.north = None       # type: Optional[Cell]
        self.south = None       # type: Optional[Cell]
        self.east = None        # type: Optional[Cell]
        self.west = None        # type: Optional[Cell]

    def link(self, cell: 'Cell', bidi: bool = True) -> None:
        ''' Link yourself to another cell '''
        self._links[cell] = True
        if bidi: cell.link(self, False)
    
    def __iadd__(self, cell: 'Cell') -> None:
        ''' Overload for the += operator with the link method '''
        self.link(cell)
        return self

    def unlink(self, cell: 'Cell', bidi: bool = True) -> None:
        ''' Unlink yourself from another cell '''
        if self.linked(cell): del self._links[cell]
        if bidi: cell.unlink(self, False)

    def __isub__(self, cell: 'Cell') -> None:
        ''' Overload for the -= operator with the unlink method '''
        self.unlink(cell)
        return self

    def linked(self, cell: 'Cell') -> bool:
        ''' Check if this cell is linked to another '''
        return cell != None and cell in self.links

    def __and__(self, other: 'Cell') -> bool:
        ''' Overload for the & operator with the linked? method '''
        return self.linked(other)

    @property
    def data(self):
        ''' Accesses the data dictionary '''
        return self._data

    # def setData(self, key, value) -> None:
    #     ''' Sets cell data '''
    #     self._data[key] = value

    def hasData(self, key) -> bool:
        ''' Checks wheter cell contains key '''
        return key in self.data.keys()

    # def getData(self, key):
    #     ''' Gets data value if present '''
    #     if self.hasData(key): return self._data[key]

    def __hash__(self) -> int:
        ''' Unique hash of the cell '''
        return hash((self.col, self.row, id(self)))

    # The following methods actually lie because don't take into account neighbors/linked-cells, but for now is enough

    def __repr__(self) -> str:
        ''' print representation '''
        ID = str(hex(id(self)))
        return 'Cell at ({},{}) with memory address of {}'.format(self.row, self.col, ID)

    def __eq__(self, other: 'Cell') -> bool:       # type: ignore
        return hash(self) == hash(other)

    def __ne__(self, other: 'Cell') -> bool:       # type: ignore
        return not self == other
