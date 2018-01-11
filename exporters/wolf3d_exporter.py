from time import gmtime, strftime
from typing import TYPE_CHECKING, Any, List, Optional, Union, cast

import pathfinders.dijkstra as Dijkstra
import pathfinders.longest_path as LongestPath
from base.colored_grid import ColoredGrid
from exporters.exporter import Exporter

if TYPE_CHECKING:
    from base.cell import Cell
    from base.grid import Grid
else:
    Cell = 'Cell'
    Grid = 'Grid'


class Wolf3DExporter(Exporter):
    '''
    Drawing logic adapted from ASCIIRenderer: Draws topmost row (northen wall), then proceeds drawing south-east.
    '''

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

    MAX_ENEMIES = 149  # limits per level: 149 enemies, 399 objects, and 64 doors

    # because LEV map columns don't align perfectly with our cells,
    # we'll fill the rightmost remaining columns of each row
    WALL_FILL = [WALL_STONE, HEX_FILL]
    OBJECT_FILL = [OBJECT_EMPTY, HEX_FILL]

    @property
    def enemies_count(self) -> int:
        return self._enemies_count

    def __init__(self) -> None:
        self._enemies_count = 0  # type: int

    def render(self, grid: Union[Grid, ColoredGrid], **kwargs: Any) -> None:
        assert isinstance(grid, ColoredGrid)

        filename = strftime('%d%H%M%S', gmtime())

        for key in kwargs:
            if key == 'filename':
                filename = kwargs[key]

        if grid.rows < self.MAP_MAX_ROWS or grid.cols < self.MAP_MAX_COLUMNS:
            grid = self._expand(grid, self.MAP_MAX_ROWS, self.MAP_MAX_COLUMNS)

        if grid.rows > self.MAP_MAX_ROWS:
            raise ValueError('Wolfenstein3D NMap only allows maps with {} rows maximum'.format(self.MAP_MAX_ROWS))
        if grid.cols > self.MAP_MAX_COLUMNS:
            raise ValueError('Wolfenstein3D NMap only allows maps with {} columns maximum'.format(self.MAP_MAX_COLUMNS))

        grid = self._store_solution(grid)

        # first row is easy as it's all wall
        walls = self.WALL_FILL + self.WALL_FILL * grid.cols * 2 + self.WALL_FILL
        objects = self.OBJECT_FILL + self.OBJECT_FILL * grid.cols * 2 + self.OBJECT_FILL

        for row in grid.eachRow():
            walls_top = [self.WALL_STONE, self.HEX_FILL]
            objects_top = [self.OBJECT_EMPTY, self.HEX_FILL]

            walls_bottom = [self.WALL_STONE, self.HEX_FILL]
            objects_bottom = [self.OBJECT_EMPTY, self.HEX_FILL]

            for cell in row:
                wall_body = self._wall_for(cell, grid)
                object_body = self._object_for(cell, grid)
                if cell & cell.east:
                    wall_east_boundary = [self.WALL_EMPTY_CELL, self.HEX_FILL]
                else:
                    wall_east_boundary = [self.WALL_STONE, self.HEX_FILL]
                walls_top += wall_body + wall_east_boundary
                objects_top += object_body + [self.OBJECT_EMPTY, self.HEX_FILL]

                if cell & cell.south:
                    wall_south_boundary = [self.WALL_EMPTY_CELL, self.HEX_FILL]
                else:
                    wall_south_boundary = [self.WALL_STONE, self.HEX_FILL]
                walls_bottom += wall_south_boundary + [self.WALL_STONE, self.HEX_FILL]
                objects_bottom += [self.OBJECT_EMPTY, self.HEX_FILL] * 2

            walls += walls_top + self.WALL_FILL
            objects += objects_top + self.OBJECT_FILL

            walls += walls_bottom + self.WALL_FILL
            objects += objects_bottom + self.OBJECT_FILL

        self._write_data(filename, walls, objects)

    @staticmethod
    def is_valid(grid: ColoredGrid) -> bool:
        ''' Wolf3D exit wall cell is a switch that only gets rendered east and west '''
        _, end = LongestPath.calculate(grid)
        cell = grid[end[0], end[1]]
        if cell is None:
            raise ValueError('Ending row not found at row {} column {}'.format(*end))
        linked_neighbor = cell.links[0]     # assume exactly one path to the exit
        return (cell.east is not None and cell.east == linked_neighbor) or \
               (cell.west is not None and cell.west == linked_neighbor)

    @staticmethod
    def _expand(grid: ColoredGrid, rows: int, cols: int) -> ColoredGrid:
        new_grid = ColoredGrid(rows, cols)
        for cell in grid.eachCell():
            new_grid[cell.row, cell.col] = cell
        return new_grid

    @staticmethod
    def _store_solution(grid: ColoredGrid) -> ColoredGrid:
        start, end = LongestPath.calculate(grid)
        grid = cast(ColoredGrid, Dijkstra.calculate_distances(grid, start, end))
        return grid

    @staticmethod
    def _write_data(filename: str, walls: List[int], objects: List[int]) -> None:
        with open(filename, 'wb') as file:
            # write walls
            file.write(bytes(walls))
            # padding with walls until exactly 8192 bytes
            padding = [Wolf3DExporter.WALL_EMPTY_CELL, Wolf3DExporter.HEX_FILL] * round((8192 - len(walls)) / 2)
            file.write(bytes(padding))

            # then write objects
            file.write(bytes(objects))
            # and again padding (which should be exactly the same)
            padding = [Wolf3DExporter.OBJECT_EMPTY, Wolf3DExporter.HEX_FILL] * round((8192 - len(objects)) / 2)
            file.write(bytes(padding))

        print('Filename: {}'.format(filename))

    @staticmethod
    def _cell_distance(cell: Cell, grid: ColoredGrid) -> Optional[int]:
        if grid.distances is not None and grid.maximum > 0 and grid.distances[cell] is not None:
            return cast(int, grid.distances[cell])
        else:
            return None

    def _wall_for(self, cell: Cell, grid: ColoredGrid) -> List[int]:
        wall = [self.WALL_EMPTY_CELL, self.HEX_FILL] if len(cell.links) > 0 else [self.WALL_STONE, self.HEX_FILL]
        distance = self._cell_distance(cell, grid)
        if distance is not None and distance == grid.maximum:
            return [self.WALL_ELEVATOR_EXIT_EW, self.HEX_FILL]
        return wall

    def _object_for(self, cell: Cell, grid: ColoredGrid) -> List[int]:
        distance = self._cell_distance(cell, grid)
        if distance is not None:
            if 0 < distance < grid.maximum:
                # main path never reaches deadends, so no need to check for cell contents
                return [self.OBJECT_EMPTY, self.HEX_FILL]
            elif distance == grid.maximum:
                # finish cell: Nothing as wall will be overriden with exit cell
                return [self.OBJECT_EMPTY, self.HEX_FILL]
            else:
                # starting cell
                linked_neighbor = cell.links[0]     # assume exactly one path to the exit
                if cell.east and cell.east == linked_neighbor:
                    return [self.OBJECT_STARTING_POSITION_FACING_E, self.HEX_FILL]
                elif cell.north and cell.north == linked_neighbor:
                    return [self.OBJECT_STARTING_POSITION_FACING_N, self.HEX_FILL]
                elif cell.west and cell.west == linked_neighbor:
                    return [self.OBJECT_STARTING_POSITION_FACING_W, self.HEX_FILL]
                else:
                    return [self.OBJECT_STARTING_POSITION_FACING_S, self.HEX_FILL]
        else:
            return self._cell_contents(cell)

    def _cell_contents(self, cell: Cell) -> List[int]:
        if len(cell.links) == 1 and self.enemies_count < self.MAX_ENEMIES:
            # dead-end
            self._enemies_count += 1
            linked_neighbor = cell.links[0]
            if cell.east and cell.east == linked_neighbor:
                return [self.OBJECT_GUARD_FACING_E, self.HEX_FILL]
            elif cell.north and cell.north == linked_neighbor:
                return [self.OBJECT_GUARD_FACING_N, self.HEX_FILL]
            elif cell.west and cell.west == linked_neighbor:
                return [self.OBJECT_GUARD_FACING_W, self.HEX_FILL]
            else:
                return [self.OBJECT_GUARD_FACING_S, self.HEX_FILL]
        else:
            return [self.OBJECT_EMPTY, self.HEX_FILL]
