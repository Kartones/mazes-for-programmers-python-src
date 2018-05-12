from abc import ABCMeta, abstractmethod

from base.grid import Grid


class Algorithm(metaclass=ABCMeta):

    @abstractmethod
    def on(self, grid: Grid) -> None:
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self.__class__.__name__
