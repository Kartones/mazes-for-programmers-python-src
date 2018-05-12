from random import randrange
from typing import Any, cast, Dict, Generator, List, Optional, Tuple

from base.cell import Cell, is_cell


Key = Tuple[int, int]
CellList = List[Cell]


class Grid:

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._columns

    @property
    def size(self) -> int:
        return self.rows * self.columns

    @property
    def dimensions(self) -> Key:
        return self.rows, self.columns

    @property
    def data(self) -> Dict:
        return self._data

    @property
    def deadends(self) -> List[Cell]:
        return [cell for cell in self.each_cell() if len(cell.links) == 1]

    def __init__(self, rows: int, columns: int) -> None:
        if rows is None or rows < 2:
            raise ValueError("Rows must be an integer greater than 1")
        if columns is None or columns < 2:
            raise ValueError("Columns must an integer greater than 1")

        self._rows: int = rows
        self._columns: int = columns
        self._data: Dict = {}
        self._grid: List[List[Cell]] = self.prepare_grid()
        self.configure_cells()

    def cell_at(self, row: int, column: int) -> Optional[Cell]:
        if not (0 <= row < self.rows):
            return None
        if not (0 <= column < self.columns):
            return None
        return self._grid[row][column]

    def set_cell_at(self, row: int, column: int, value: Cell) -> None:
        self._grid[row][column] = value

    def prepare_grid(self) -> List[List[Cell]]:
        return [[Cell(row, column) for column in range(self.columns)] for row in range(self.rows)]

    def configure_cells(self) -> None:
        """
        Create all the north/sout/east/west dependencies of the cells
        """
        for cell in self.each_cell():
            row = cell.row
            column = cell.column

            cell.north = self[row - 1, column]
            cell.south = self[row + 1, column]
            cell.east = self[row, column + 1]
            cell.west = self[row, column - 1]

    def random_cell(self) -> Cell:
        row = randrange(0, self.rows)
        column = randrange(0, self.columns)
        return cast(Cell, self[row, column])

    def each_row(self) -> Generator[CellList, None, None]:
        for row in range(self.rows):
            yield self._grid[row]

    # TODO: Add tests
    def each_column(self) -> Generator[CellList, None, None]:
        for column in zip(*self._grid):
            yield column

    def each_cell(self) -> Generator:
        for row in self.each_row():
            for cell in row:
                yield cell

    def contents_of(self, cell: Cell) -> str:
        return "   "

    def __getitem__(self, key: Key) -> Optional[Cell]:
        if not is_key(key):
            raise IndexError('Only grid[row,col] __getitem__ calls are supported')
        return self.cell_at(*key)

        if is_key(key):
            row, column = key
            if row < 0 or row > self.rows - 1:
                return None
            if column < 0 or column > self.columns - 1:
                return None
            return self._grid[row][column]

    def __setitem__(self, key: Key, value: Cell) -> None:
        if not (is_key(key) and is_cell(value)):
            raise IndexError('Only grid[row,col] __setitem__ calls are supported')
        self.set_cell_at(*key, value)

    def __contains__(self, other: Cell) -> bool:
        if is_cell(other):
            for cell in self.each_cell():
                if cell == other:
                    return True
        return False


def is_key(key: Key) -> bool:
    """
    Runtime check for key correctness
    """
    return type(key) == tuple and len(key) == 2 and not any(type(value) != int for value in key)


def is_grid(grid: Any) -> bool:
    return isinstance(grid, Grid)
