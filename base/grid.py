from random import randrange
from typing import Any, Dict, Generator, Hashable, List, Optional, Tuple, cast

from base.cell import Cell

Key = Tuple[int, int]
ListOfCells = List[Cell]


class Grid:

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def size(self) -> int:
        return self.rows * self.cols

    @property
    def shape(self) -> Key:
        return self.rows, self.cols

    @property
    def deadends(self) -> ListOfCells:
        return [cell for cell in self.eachCell() if len(cell.links) == 1]

    @property
    def data(self) -> Dict:
        ''' Accesses the data dictionary '''
        return self._data

    def __init__(self, rows: int, cols: int) -> None:
        if rows is None or rows < 2:
            raise ValueError('Rows must be an integer greater than 1')
        if cols is None or cols < 2:
            raise ValueError('cols must an integer greater than 1')

        self._rows = rows  # type: int
        self._cols = cols  # type: int
        self._data = {}  # type: dict
        self._grid = self.prepareGrid()  # type: List[List[Cell]]
        self.configureCells()

    def prepareGrid(self) -> List[List[Cell]]:
        ''' Create the grid '''
        return [[Cell(row, column) for column in range(self.cols)] for row in range(self.rows)]

    def configureCells(self) -> None:
        ''' Create all the north/sout/east/west dependencies of the cells '''
        for cell in self.eachCell():
            row = cell.row
            col = cell.col

            cell.north = cast(Cell, self[row - 1, col])
            cell.south = self[row + 1, col]
            cell.east = self[row, col + 1]
            cell.west = self[row, col - 1]

    def __getitem__(self, key: Key) -> Optional[Cell]:
        ''' Get grid item method '''
        if self._isCorrectKey(key):
            row, col = key
            if row < 0 or row > self.rows - 1: return None
            if col < 0 or col > self.cols - 1: return None
            return self._grid[row][col]
        else:
            raise IndexError('Only grid[row,col] __getitem__ calls are supported')

    def __setitem__(self, key: Key, item: Cell) -> None:
        ''' Set grid item method '''
        if self._isCorrectKey(key) and isinstance(item, Cell):
            row, col = key
            if 0 <= row <= self.rows - 1 and 0 <= col <= self.cols - 1:
                self._grid[row][col] = item
        else:
            raise IndexError('Only grid[row,col] __setitem__ calls are supported')

    def randomCell(self) -> Cell:
        ''' Return random cell '''
        row = randrange(0, self.rows)
        col = randrange(0, self.cols)
        return cast(Cell, self[row, col])

    def eachRow(self) -> Generator[ListOfCells, None, None]:
        ''' Access each row '''
        for row in self._grid:
            yield row

    def eachCol(self) -> Generator[ListOfCells, None, None]:
        ''' Access each column '''
        for col in zip(*self._grid):
            yield col

    def eachCell(self) -> Generator[Cell, None, None]:
        ''' Access each cell '''
        for row in self.eachRow():
            for cell in row:
                yield cell

    def prepareCellData(self, key: Hashable, value: Any = None) -> None:
        ''' Prepares the _data of the cells '''
        for cell in self.eachCell():
            cell.data[key] = value

    def contents(self, cell: Cell) -> str:
        return '   '

    @staticmethod
    def _isCorrectKey(key: Key) -> bool:
        ''' Runtime check for key correctness '''
        return type(key) == tuple and len(key) == 2 and not any(type(x) != int for x in key)
