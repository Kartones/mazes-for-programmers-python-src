from abc import ABCMeta, abstractmethod
from typing import Any, Union, Dict  # noqa: F401

from base.grid import Grid
from base.cell import Cell

DIRECTIONS = ['north', 'n', 'south', 's', 'east', 'e', 'west', 'w']


class Algorithm(metaclass=ABCMeta):
    ''' Base algorithm metaclass '''

    def __init__(self) -> None:
        self.step_count = 0  # type: int

    @abstractmethod
    def on(self, grid: Grid) -> None:
        ''' Run the algorithm '''
        raise NotImplementedError

    def step(self, value: int = 1) -> None:
        ''' Step the count of the algorithm '''
        self.step_count += value

    @property
    def name(self) -> str:
        ''' Name of the algorithm '''
        return self.__class__.__name__


class AlgorithmWithLogging(Algorithm, metaclass=ABCMeta):
    ''' Base algorithm metaclass with logging '''

    def __init__(self, log: bool = True) -> None:
        super().__init__()
        self.log = log

    def _prepareLogGrid(self, grid: Grid) -> None:
        ''' Prepare the grid for logging the algorithm '''
        if not self.log: return
        # 'visit' : List of steps on which the cell was visited
        # 'links' : Directions of the links made by the cell (NOT to the cell)
        data = {'visit': [], 'links': []}  # type: Dict
        key = self.name  # type: str
        for cell in grid.eachCell():
            cell.data[key] = data

    def _logVisit(self, cell: Cell) -> None:
        ''' Log the step number on which the cell was visited '''
        if not self.log: return
        cell.data[self.name]['visit'].append(self.step_count)

    def _logLink(self, cell: Cell, other: Cell) -> None:
        ''' Log the direction in which the cell made links on the step specified by the number '''
        if not self.log: return

        step_count = self.step_count

        if other == cell.north:
            cell.data[self.name]['links'].append((step_count, 'north'))
        elif other == cell.south:
            cell.data[self.name]['links'].append((step_count, 'south'))
        elif other == cell.east:
            cell.data[self.name]['links'].append((step_count, 'east'))
        elif other == cell.west:
            cell.data[self.name]['links'].append((step_count, 'west'))
