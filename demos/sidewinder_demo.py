
from base.grid import Grid
from algorithms.sidewinder import Sidewinder
from renderers.ascii_renderer import ASCIIRenderer


if __name__ == "__main__":
    grid = Grid(6, 6)
    grid = Sidewinder.on(grid)
    ASCIIRenderer.render(grid)
