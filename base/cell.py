import warnings
from random import choice
from typing import Any, Dict, Hashable, List, Optional, cast, Tuple

from base.distances import Distances

Links = Dict['Cell', bool]
ListOfCells = List['Cell']
TwoCells = Tuple['Cell', 'Cell']


class Cell:

    @property
    def links(self) -> ListOfCells:
        return list(self._links.keys())

    @property
    def neighbours(self) -> ListOfCells:
        ''' List of neighbours '''
        neighbours = []  # type: ListOfCells
        if self.north: neighbours.append(self.north)
        if self.south: neighbours.append(self.south)
        if self.east: neighbours.append(self.east)
        if self.west: neighbours.append(self.west)
        return neighbours

    def randomNeighbour(self) -> Optional['Cell']:
        ''' Return a random neighbour '''
        if self.nNeighbours == 0: return None
        return choice(self.neighbours)

    @property
    def nLinks(self) -> int:
        ''' Number of links '''
        return len(self.links)

    @property
    def nNeighbours(self) -> int:
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
            raise ValueError('Row must be a positive integer')
        if col is None or col < 0:
            raise ValueError('Column must be a positive integer')

        self.row = row     # type: int
        self.col = col     # type: int
        self._links = {}   # type: Links
        self._data = {}    # type: Dict
        self.north = None  # type: Optional[Cell]
        self.south = None  # type: Optional[Cell]
        self.east = None   # type: Optional[Cell]
        self.west = None   # type: Optional[Cell]

    def link(self, cell: 'Cell', bidi: bool = True) -> None:
        ''' Link yourself to another cell '''
        if isCell(cell):
            self._links[cell] = True
            if bidi: cell.link(self, False)
        else:
            raise ValueError('Link can be made/broken only between two cells')

    def __iadd__(self, cell: 'Cell') -> 'Cell':
        ''' Overload for the += operator with the link method '''
        self.link(cell)
        return self

    def unlink(self, cell: Optional['Cell'], bidi: bool = True) -> None:
        ''' Unlink yourself from another cell '''
        if isCell(cell):
            if cell in self.links:
                del self._links[cell]
                if bidi: cell.unlink(self, False)
        elif cell is None:
            warnings.warn('Attempted link to None. No link has been made.', UserWarning)
        else:
            raise ValueError('Link can be made/broken only between two cells')

    def __isub__(self, cell: 'Cell') -> 'Cell':
        ''' Overload for the -= operator with the unlink method '''
        self.unlink(cell)
        return self

    def linked(self, cell: Optional['Cell']) -> bool:
        ''' Check if this cell is linked to another '''
        if isCell(cell):
            return cell in self.links
        elif cell is None:
            return False
        else:
            raise ValueError('Cells can be linked only to other cells')

    def __and__(self, other: Optional['Cell']) -> bool:
        ''' Overload for the & operator with the linked? method '''
        return self.linked(other)

    @property
    def data(self) -> Dict:
        ''' Accesses the data dictionary '''
        return self._data

    def hasData(self, key: Hashable) -> bool:
        ''' Checks wheter cell contains key '''
        return key in self.data.keys()

    def __hash__(self) -> int:
        ''' Unique hash of the cell '''
        # return hash((self.col, self.row, id(self)))
        return hash((self.col, self.row))

    def __repr__(self) -> str:
        ''' Representation of cell for print()/format() calls '''
        ID = str(hex(id(self)))
        return 'Cell at ({},{}) with memory address of {}'.format(self.row, self.col, ID)

    # The following methods actually lie because don't take into account neighbors/linked-cells, but for now is enough

    def __eq__(self, other: Any) -> bool:
        if isCell(other):
            return hash(self) == hash(other)
        else:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self == other


def isCell(cell: Any) -> bool:
    ''' Runtime class check '''
    return isinstance(cell, Cell)
