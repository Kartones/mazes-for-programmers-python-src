from time import gmtime, strftime

from typing import Any, cast, List, Optional

from base.cell import Cell
from base.colored_grid import ColoredGrid

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath


HEX_FILL = 0x00

# always add a 0x00 byte afterwards to all wall and objects
WALL_STONE = 0x01
WALL_EMPTY_CELL = 0x6c
WALL_ELEVATOR_EXIT_EW = 0x15

OBJECT_EMPTY = 0x00
OBJECT_STARTING_POSITION_FACING_N = 0x13
OBJECT_STARTING_POSITION_FACING_E = 0x14
OBJECT_STARTING_POSITION_FACING_S = 0x15
OBJECT_STARTING_POSITION_FACING_W = 0x16
OBJECT_GUARD_FACING_E = 0x6c
OBJECT_GUARD_FACING_N = 0x6d
OBJECT_GUARD_FACING_W = 0x6e
OBJECT_GUARD_FACING_S = 0x6f

# As our cells are bigger than 1 wolf3D cell (ours being 2x2), maps are smaller
MAP_MAX_ROWS = 31
MAP_MAX_COLUMNS = 31

MAX_ENEMIES = 149   # limits per level: 149 enemies, 399 objects, and 64 doors

# because LEV map columns don't align perfectly with our cells,
# we'll fill the rightmost remaining columns of each row
WALL_FILL = [WALL_STONE, HEX_FILL]
OBJECT_FILL = [OBJECT_EMPTY, HEX_FILL]


"""
Drawing logic adapted from ASCIIRenderer: Draws topmost row (northen wall), then proceeds drawing south-east.
"""


class Wolf3DRenderer:

    @property
    def enemies_count(self) -> int:
        return self._enemies_count  # type: ignore

    def __init__(self) -> None:
        self._enemies_count = 0

    def expand(self, grid: ColoredGrid, rows: int, columns: int) -> ColoredGrid:
        new_grid = ColoredGrid(rows, columns)
        for cell in grid.each_cell():
            new_grid.set_cell_at(cell.row, cell.column, cell)
        return new_grid

    def store_solution(self, grid: ColoredGrid) -> ColoredGrid:
        start_row, start_column, end_row, end_column = LongestPath.calculate(grid)
        grid = cast(ColoredGrid, Dijkstra.calculate_distances(grid, start_row, start_column, end_row, end_column))
        return grid

    def write_data(self, filename: str, walls: List[int], objects: List[int]) -> None:
        with open(filename, "wb") as file:
            # write walls
            file.write(bytes(walls))
            # padding with walls until exactly 8192 bytes
            padding = [WALL_EMPTY_CELL, HEX_FILL] * round((8192 - len(walls)) / 2)
            file.write(bytes(padding))

            # then write objects
            file.write(bytes(objects))
            # and again padding (which should be exactly the same)
            padding = [OBJECT_EMPTY, HEX_FILL] * round((8192 - len(objects)) / 2)
            file.write(bytes(padding))

        print("Filename: {}".format(filename))

    def cell_distance(self, cell: Cell, grid: ColoredGrid) -> Optional[int]:
        if grid.distances is not None and grid.maximum > 0 and grid.distances[cell] is not None:
            return cast(int, grid.distances[cell])
        else:
            return None

    def wall_for(self, cell: Cell, grid: ColoredGrid) -> List[int]:
        wall = [WALL_EMPTY_CELL, HEX_FILL] if len(cell.links) > 0 else [WALL_STONE, HEX_FILL]
        distance = self.cell_distance(cell, grid)
        if distance is not None and distance == grid.maximum:
            return [WALL_ELEVATOR_EXIT_EW, HEX_FILL]
        return wall

    def object_for(self, cell: Cell, grid: ColoredGrid) -> List[int]:
        distance = self.cell_distance(cell, grid)
        if distance is not None:
            if 0 < distance < grid.maximum:
                # main path never reaches deadends, so no need to check for cell contents
                return [OBJECT_EMPTY, HEX_FILL]
            elif distance == grid.maximum:
                # finish cell: Nothing as wall will be overriden with exit cell
                return [OBJECT_EMPTY, HEX_FILL]
            else:
                # starting cell
                linked_neighbor = cell.links[0]     # assume exactly one path to the exit
                if (cell.east and cell.east == linked_neighbor):
                    return [OBJECT_STARTING_POSITION_FACING_E, HEX_FILL]
                elif (cell.north and cell.north == linked_neighbor):
                    return [OBJECT_STARTING_POSITION_FACING_N, HEX_FILL]
                elif (cell.west and cell.west == linked_neighbor):
                    return [OBJECT_STARTING_POSITION_FACING_W, HEX_FILL]
                else:
                    return [OBJECT_STARTING_POSITION_FACING_S, HEX_FILL]
        else:
            return self.cell_contents(cell, grid)

    def cell_contents(self, cell: Cell, grid: ColoredGrid) -> List[int]:
        if len(cell.links) == 1 and self.enemies_count < MAX_ENEMIES:
            # TODO: See if can use grid.deadends just caching them and comparing cell against them
            # dead-end
            self._enemies_count += 1
            linked_neighbor = cell.links[0]
            if (cell.east and cell.east == linked_neighbor):
                return [OBJECT_GUARD_FACING_E, HEX_FILL]
            elif (cell.north and cell.north == linked_neighbor):
                return [OBJECT_GUARD_FACING_N, HEX_FILL]
            elif (cell.west and cell.west == linked_neighbor):
                return [OBJECT_GUARD_FACING_W, HEX_FILL]
            else:
                return [OBJECT_GUARD_FACING_S, HEX_FILL]
        else:
            return [OBJECT_EMPTY, HEX_FILL]

    def is_valid(self, grid: ColoredGrid) -> bool:
        """
        Wolf3D exit wall cell is a switch that only gets rendered east and west
        """
        _, _, end_row, end_column = LongestPath.calculate(grid)
        cell = grid.cell_at(end_row, end_column)
        if cell is None:
            raise ValueError("Ending row not found at row {} column {}".format(end_row, end_column))
        linked_neighbor = cell.links[0]     # assume exactly one path to the exit
        return (cell.east is not None and cell.east == linked_neighbor) or \
               (cell.west is not None and cell.west == linked_neighbor)

    def render(self, grid: ColoredGrid, **kwargs: Any) -> None:
        filename = strftime("%d%H%M%S", gmtime())

        for key in kwargs:
            if key == "filename":
                filename = kwargs[key]

        if grid.rows < MAP_MAX_ROWS or grid.columns < MAP_MAX_COLUMNS:
            grid = self.expand(grid, MAP_MAX_ROWS, MAP_MAX_COLUMNS)

        if grid.rows > MAP_MAX_ROWS:
            raise ValueError("Wolfenstein3D NMap only allows maps with {} rows maximum".format(MAP_MAX_ROWS))
        if grid.columns > MAP_MAX_COLUMNS:
            raise ValueError("Wolfenstein3D NMap only allows maps with {} columns maximum".format(MAP_MAX_COLUMNS))

        grid = self.store_solution(grid)

        # first row is easy as it's all wall
        walls = WALL_FILL + WALL_FILL * grid.columns * 2 + WALL_FILL
        objects = OBJECT_FILL + OBJECT_FILL * grid.columns * 2 + OBJECT_FILL

        for row in grid.each_row():
            walls_top = [WALL_STONE, HEX_FILL]
            objects_top = [OBJECT_EMPTY, HEX_FILL]

            walls_bottom = [WALL_STONE, HEX_FILL]
            objects_bottom = [OBJECT_EMPTY, HEX_FILL]

            for cell in row:
                wall_body = self.wall_for(cell, grid)
                object_body = self.object_for(cell, grid)
                wall_east_boundary = \
                    [WALL_EMPTY_CELL, HEX_FILL] if cell.linked_to(cell.east) else [WALL_STONE, HEX_FILL]
                walls_top += wall_body + wall_east_boundary
                objects_top += object_body + [OBJECT_EMPTY, HEX_FILL]

                wall_south_boundary = \
                    [WALL_EMPTY_CELL, HEX_FILL] if cell.linked_to(cell.south) else [WALL_STONE, HEX_FILL]
                walls_bottom += wall_south_boundary + [WALL_STONE, HEX_FILL]
                objects_bottom += [OBJECT_EMPTY, HEX_FILL] * 2

            walls += walls_top + WALL_FILL
            objects += objects_top + OBJECT_FILL

            walls += walls_bottom + WALL_FILL
            objects += objects_bottom + OBJECT_FILL

        self.write_data(filename, walls, objects)
