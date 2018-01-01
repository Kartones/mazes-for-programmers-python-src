from abc import ABCMeta, abstractmethod
from typing import Any, Union, List

from base.grid import Grid
from base.cell import Cell
from base.colored_grid import ColoredGrid

DIRECTIONS = ['north', 'n', 'south', 's', 'east', 'e', 'west', 'w']

class Algorithm(metaclass=ABCMeta):
    ''' Base algorithm metaclass '''

    def __init__(self):
        self.step_count = 0

    @abstractmethod
    def on(self, grid: Union[Grid, ColoredGrid], ** kwargs: Any) -> None:
        ''' Run the algorithm '''
        raise NotImplementedError

    def step(self, value=1):
        ''' Step the count of the algorithm '''
        self.step_count += value

class AlgorithmWithLogging(Algorithm, metaclass=ABCMeta):
    ''' Base algorithm metaclass with logging '''
    
    def __init__(self, *args, log=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = log
    
    @property
    def name(self):
        ''' Name of the algorithm '''
        return self.__class__.__name__

    def _prepareLogGrid(self, grid: Grid) -> None:
        ''' Prepare the grid for logging the algorithm '''
        if not self.log: return
        data = {'visit':   [], # List of steps on which the cell was visited
                'links':   []} # Directions of the links made by the cell and(NOT to the cell)
        grid.prepareCellData(self.name, data)

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