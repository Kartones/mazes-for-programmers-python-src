from itertools import chain
from random import randrange
import random
from typing import Dict, cast, Generator, List, Optional, Tuple

from base.cell import Cell, is_cell
from base.distances import Distances
from base.grid import Grid


Key = Tuple[int, int, int]
CellList = List["Cell3d"]

class Cell3d(Cell):
    @property
    def level(self) -> int:
        return self._level

    @property
    def neighbors(self) -> CellList:
        neighbors_list: CellList = super().neighbors
        if self.up:
            neighbors_list.append(self.up)
        if self.down:
            neighbors_list.append(self.down)
        return neighbors_list

    def __init__(self, level:int, row: int, column: int) -> None:
        if level is None or level < -1: # -1 is a special cell used for drawing blanks
            raise ValueError("Level must be a positive integer")
        if row is None or row < -1: # -1 is a special cell used for drawing blanks
            raise ValueError("Row must be a positive integer")
        if column is None or column < -1: # -1 is a special cell used for drawing blanks
            raise ValueError("Column must be a positive integer")

        self._level: int = level
        self._row: int = row
        self._column: int = column
        self._links: Dict[Cell3d, bool] = {}
        self._data: Dict = {}
        self.north: Optional[Cell3d] = None
        self.south: Optional[Cell3d] = None
        self.east: Optional[Cell3d] = None
        self.west: Optional[Cell3d] = None
        self.up: Optional[Cell3d] = None
        self.down: Optional[Cell3d] = None

    def linked_to(self, cell: Optional["Cell3d"]) -> bool:
        if is_cell(cell):
            return cell in self._links
        elif cell is None:
            return False
        else:
            raise ValueError("Attempted to check link with non-cell")

    def __hash__(self) -> int:
        return hash((self.level, self.column, self.row))

    def __repr__(self) -> str:
        return "({},{},{}) = {}".format(self.level,self.column, self.row, str(hex(id(self))))

class Grid3d(Grid):

    @property
    def levels(self) -> int:
        return self._levels

    @property
    def distances(self) -> Optional[Distances]:
        return self._distances

    @property
    def size(self) -> int:
        return self.levels * self.rows * self.columns

    def __init__(self, levels: int, rows: int, columns: int) -> None:
        self._levels = levels
        super().__init__(rows, columns)
        self._distances: Optional[Distances] = None
        self.maximum: int = 0

    @distances.setter
    def distances(self, value: Optional[Distances]) -> None:
        self._distances = value
        if self._distances:
            _, self.maximum = self._distances.max

    def contents_of(self, cell: Cell) -> str:
        if self.distances is not None and self.distances[cell] is not None:
            return format(self.distances[cell], "02X").center(2)
        else:
            if cell.level == -1 and cell.row == -1 and cell.column == -1:
                return "XX"
            else:
                return "  "

    def prepare_grid(self) -> List[List[List[Cell3d]]]:
        return [[[Cell3d(level, row, column) for column in range(self.columns)] for row in range(self.rows)] for level in range(self.levels)]

    def configure_cells(self) -> None:
        """
        Create all the north/sout/east/west dependencies of the cells
        """
        for cell in self.each_cell():
            level = cell.level
            row = cell.row
            column = cell.column

            cell.north = self[level, row - 1, column]
            cell.south = self[level, row + 1, column]
            cell.east = self[level, row, column + 1]
            cell.west = self[level, row, column - 1]
            cell.down = self[level - 1, row, column]
            cell.up = self[level + 1, row, column]

    def cell_at(self, level: int, row: int, column: int) -> Optional[Cell3d]:
        if not (0 <= level < self.levels):
            return None
        if not (0 <= row < self.rows):
            return None
        if not (0 <= column < self.columns):
            return None
        return self._grid[level][row][column]

    def random_cell(self) -> Cell3d:
        level = randrange(0, self.levels)
        row = randrange(0, self.rows)
        column = randrange(0, self.columns)
        return cast(Cell3d, self[level, row, column])

    def each_level(self) -> Generator[CellList, None, None]:
        for level in range(self.levels):
            yield self._grid[level]

    def each_row(self) -> Generator[CellList, None, None]:
        for row in range(self.rows):
            yield self._grid[row]

    def nested_each_row(self) -> Generator[Cell3d, None, None]:
        for level in self.each_level():
            yield self.each_row_in_level(level)

    def each_row_in_level(self, level) -> Generator[Cell3d, None, None]:
            for row in level:
                yield row

    def each_cell(self) -> Generator[Cell3d, None, None]:
        return chain.from_iterable(self.nested_each_cell())

    def nested_each_cell(self) -> Generator[Cell3d, None, None]:
        for level in self.each_level():
            for row in self.each_row_in_level(level):
                yield self.each_cell_in_row(row)

    def each_cell_in_row(self, row) -> Generator[Cell3d, None, None]:
            for cell in row:
                yield cell

    def __getitem__(self, key: Key) -> Optional[Cell3d]:
        if not is_key(key):
            raise IndexError('Only grid[level,row,col] __getitem__ calls are supported')
        return self.cell_at(*key)


def is_key(key: Key) -> bool:
    """
    Runtime check for key correctness
    """
    return type(key) == tuple and len(key) == 3 and not any(type(value) != int for value in key)