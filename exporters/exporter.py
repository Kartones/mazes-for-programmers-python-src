from abc import ABCMeta, abstractmethod
from typing import Any

from base.grid import Grid
# from base.colored_grid import ColoredGrid


class Exporter(metaclass=ABCMeta):
    ''' Base exporter '''

    @abstractmethod
    def render(self, grid: Grid, **kwargs: Any) -> None:
        raise NotImplementedError

    @property
    def name(self) -> str:
        ''' Name of the exporter '''
        return self.__class__.__name__
