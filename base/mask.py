from random import randrange
from typing import Any, Generator, List, Optional, Tuple

Key = Tuple[int, int]
BoolList = List[bool]

class Mask:

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._columns

    def __init__(self, rows: int, columns: int) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self._bits: List[List[bool]] =  [[True for column in range(self._columns)] for row in range(self._rows)]
        # print(self._bits.each_cell].count(True))
        # self._bits[0][0] = True
        self._bits[1][1] = False
        self._bits[1][2] = False
        # print(self._bits[0].count(True))
        # print(sum([1,2]))

    def count(self) -> int:
        return list(self.each_cell()).count(True)
        # return 1


    def __getitem__(self, key: Key) -> Optional[bool]:
        # if row.between?(0, @rows - 1) && column.between?(0, @columns - 1)
        if not is_key(key):
            raise IndexError('Only mask[row,col] __getitem__ calls are supported')
        return self.cell_at(*key)

    def __setitem__(self, key: Key, value: bool) -> None:
        if not (is_key(key) and is_cell(value)):
            raise IndexError('Only mask[row,col] __setitem__ calls are supported')
        self.set_cell_at(*key, value)

    def cell_at(self, row: int, column: int) -> Optional[bool]:
        if not (0 <= row < self._rows):
            return None
        if not (0 <= column < self._columns):
            return None
        return self._bits[row][column]

    def set_cell_at(self, row: int, column: int, value: bool) -> None:
        self._grid[row][column] = value


    def each_row(self) -> Generator[BoolList, None, None]:
        for row in range(self._rows):
            yield self._bits[row]

    def each_cell(self) -> Generator:
        for row in self.each_row():
            for cell in row:
                yield cell

    def random_cell(self) -> Tuple[int ,int]:
        ret = False
        while not ret:
            row = randrange(0, self._rows)
            column = randrange(0, self._columns)
            if self.cell_at(row, column) is True:
                return [row, column]
        

def is_cell(cell: Any) -> bool:
    return isinstance(cell, bool)

def is_key(key: Key) -> bool:
    """
    Runtime check for key correctness
    """
    return type(key) == tuple and len(key) == 2 and not any(type(value) != int for value in key)