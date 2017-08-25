from random import randint
from typing import cast, Generator, List, Optional

from base.cell import Cell


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
    def deadends(self) -> List[Cell]:
        deadends_list = []
        for cell in self.each_cell():
            if len(cell.links) == 1:
                deadends_list.append(cell)
        return deadends_list

    def __init__(self, rows: int, columns: int) -> None:
        if rows is None or rows < 2:
            raise ValueError("Rows must be an integer greater than 1")
        if columns is None or columns < 2:
            raise ValueError("Columns must an integer greater than 1")

        self._rows = rows           # type: int
        self._columns = columns     # type: int
        self._grid = self.prepare_grid()
        self.configure_cells()

    def cell_at(self, row: int, column: int) -> Optional[Cell]:
        if not (0 <= row < self.rows):
            return None
        if not (0 <= column < self.columns):
            return None
        return self._grid[row][column]

    def set_cell_at(self, row: int, column: int, cell: Cell) -> None:
        self._grid[row][column] = cell

    def prepare_grid(self) -> List[List[Cell]]:
        return [[Cell(row, column) for column in range(self.columns)] for row in range(self.rows)]

    def configure_cells(self) -> None:
        for cell in self.each_cell():
            cell.north = self.cell_at(cell.row - 1, cell.column)
            cell.south = self.cell_at(cell.row + 1, cell.column)
            cell.east = self.cell_at(cell.row, cell.column + 1)
            cell.west = self.cell_at(cell.row, cell.column - 1)

    def random_cell(self) -> Cell:
        column = randint(0, self.columns - 1)
        row = randint(0, self.rows - 1)
        return cast(Cell, self.cell_at(row, column))

    def each_row(self) -> Generator:
        for row in range(self.rows):
            yield self._grid[row]

    def each_cell(self) -> Generator:
        for row in range(self.rows):
            for column in range(self.columns):
                yield self.cell_at(row, column)

    def contents_of(self, cell: Cell) -> str:
        return "   "
