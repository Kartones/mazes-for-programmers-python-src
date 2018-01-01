from abc import ABCMeta, abstractmethod
from typing import Any, Union

from base.grid import Grid
from base.colored_grid import ColoredGrid

class Exporter(metaclass=ABCMeta):
    ''' Base exporter '''

    @abstractmethod
    def render(self, grid: Union[Grid, ColoredGrid], ** kwargs: Any) -> None:
        raise NotImplementedError
