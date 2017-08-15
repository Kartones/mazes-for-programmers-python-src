
from base.grid import Grid
from algorithms.binary_tree import BinaryTree
from renderers.ascii_renderer import ASCIIRenderer


if __name__ == "__main__":
    grid = Grid(6, 6)
    grid = BinaryTree.on(grid)
    ASCIIRenderer.render(grid)
