#!/usr/bin/env python3

import random


class Cell():
    def __init__(self):
        self.visited = False
        self.blocked = False  # for 42 pattern
        self.walls = {
            "north": True,
            "east": True,
            "south": True,
            "west": True
        }


class MazeGenerator():
    def __init__(self, config):
        self.seed = config["SEED"]
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.perfect = config["PERFECT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]

    def _set_42_pattern(self, maze):
        pattern_width = 7
        pattern_height = 5
        if self.height <= pattern_width and self.width <= pattern_height:
            print('Error: Maze too small to embed the "42" pattern.')
        else:
            if self.height == 6 and self.width == 8:
                y = 0
                x = 0
            else:
                # pattern`s top left position
                y = self.height // 2 - pattern_height // 2
                x = self.width // 2 - pattern_width // 2
                print(x, y)
            # pattern "4"
            maze[y][x].blocked = True
            maze[y+1][x].blocked = True
            maze[y+2][x].blocked = True
            maze[y+2][x+1].blocked = True
            maze[y+2][x+2].blocked = True
            maze[y+3][x+2].blocked = True
            maze[y+4][x+2].blocked = True
            # pattern "2"
            maze[y][x+4].blocked = True
            maze[y][x+5].blocked = True
            maze[y][x+6].blocked = True
            maze[y+1][x+6].blocked = True
            maze[y+2][x+6].blocked = True
            maze[y+2][x+5].blocked = True
            maze[y+2][x+4].blocked = True
            maze[y+3][x+4].blocked = True
            maze[y+4][x+4].blocked = True
            maze[y+4][x+5].blocked = True
            maze[y+4][x+6].blocked = True
        return maze

    def _get_starting_point(self, maze):
        non_blocked_sells = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                if not maze[y][x].blocked:
                    non_blocked_sells.append([x, y])
        return non_blocked_sells

    def _get_unvisited_neighbors(self, x, y, maze):
        unvisited_neighbors = []

        if y > 0:
            if not maze[y - 1][x].visited and not maze[y - 1][x].blocked:
                unvisited_neighbors.append({"y": y-1,
                                            "x": x,
                                            "neighbors_direction": "south",
                                            "current_cell_direction": "north"})
        if y < self.height - 1:
            if not maze[y + 1][x].visited and not maze[y + 1][x].blocked:
                unvisited_neighbors.append({"y": y+1,
                                            "x": x,
                                            "neighbors_direction": "north",
                                            "current_cell_direction": "south"})
        if x > 0:
            if not maze[y][x - 1].visited and not maze[y][x - 1].blocked:
                unvisited_neighbors.append({"y": y,
                                            "x": x-1,
                                            "neighbors_direction": "east",
                                            "current_cell_direction": "west"})
        if x < self.width - 1:
            if not maze[y][x + 1].visited and not maze[y][x + 1].blocked:
                unvisited_neighbors.append({"y": y,
                                            "x": x+1,
                                            "neighbors_direction": "west",
                                            "current_cell_direction": "east"})
        return unvisited_neighbors

    def has_open_3x3(self, maze, x, y):
        def is_open_3x3(maze, x, y):
            # x,y - top left corner position of 3x3 area
            # reject windows starting outside the maze
            if x < 0 or y < 0:
                return False
            # check all 6 horizontal (south) walls
            for yy in range(y, y + 2):
                for xx in range(x, x + 3):
                    try:
                        if maze[yy][xx].walls["south"]:
                            return False
                    except IndexError:
                        return False

            # check all 6 vertical (east) walls
            for yy in range(y, y + 3):
                for xx in range(x, x + 2):
                    try:
                        if maze[yy][xx].walls["east"]:
                            return False
                    except IndexError:
                        return False

            return True

        # check all 9 3x3 areas around given cell
        for yy in range(y - 2, y + 1):
            for xx in range(x - 2, x + 1):
                if is_open_3x3(maze, xx, yy):
                    return True

        return False

    def _remove_random_walls(self, maze, walls_num):
        removed = 0
        # to avoid cases when i cant remove given number of walls
        # without creating 3x3 hall
        count_3x3_open_areas = 0
        while removed < walls_num and count_3x3_open_areas < 5:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if maze[y][x].blocked:
                continue

            neighbors = []

            if y > 0:
                neighbors.append({"y": y-1,
                                  "x": x,
                                  "neighbors_direction": "south",
                                  "current_cell_direction": "north"})
            if y < self.height - 1:
                neighbors.append({"y": y+1,
                                  "x": x,
                                  "neighbors_direction": "north",
                                  "current_cell_direction": "south"})
            if x > 0:
                neighbors.append({"y": y,
                                  "x": x-1,
                                  "neighbors_direction": "east",
                                  "current_cell_direction": "west"})
            if x < self.width - 1:
                neighbors.append({"y": y,
                                  "x": x+1,
                                  "neighbors_direction": "west",
                                  "current_cell_direction": "east"})

            neighbor = random.choice(neighbors)
            if maze[neighbor["y"]][neighbor["x"]].blocked:
                continue
            if maze[y][x].walls[neighbor["current_cell_direction"]]:
                maze[y][x].walls[neighbor["current_cell_direction"]] = False
                (maze[neighbor["y"]][neighbor["x"]]
                 .walls[neighbor["neighbors_direction"]]) = False
                if self.has_open_3x3(maze, x, y) or \
                   self.has_open_3x3(maze, neighbor["x"], neighbor["y"]):
                    maze[y][x].walls[neighbor["current_cell_direction"]] = True
                    (maze[neighbor["y"]][neighbor["x"]]
                     .walls[neighbor["neighbors_direction"]]) = True
                    count_3x3_open_areas += 1
                else:
                    removed += 1
        return maze

    def _cells_to_integers(self, maze):
        maze_integer = [[] * self.width] * self.height
        for y in range(self.height):
            maze_integer[y] = []
            for x in range(self.width):
                value = 0
                if maze[y][x].walls["north"]:
                    value = value | 1
                if maze[y][x].walls["east"]:
                    value = value | 2
                if maze[y][x].walls["south"]:
                    value = value | 4
                if maze[y][x].walls["west"]:
                    value = value | 8
                maze_integer[y].append(value)
        return maze_integer

    def generate(self, seed=None) -> list[list[int]]:
        if seed is not None:
            random.seed(seed)
        else:
            random.seed(self.seed)

        maze = [[Cell() for i in range(self.width)]
                for j in range(self.height)]
        maze = self._set_42_pattern(maze)
        if maze[self.entry[1]][self.entry[0]].blocked or \
           maze[self.exit[1]][self.exit[0]].blocked:
            raise ValueError("Entry and exit points must be out of 42 pattern")
        not_bloked_cells = self._get_starting_point(maze)
        x, y = random.choice(not_bloked_cells)
        maze[y][x].visited = True

        stack = []  # to save visited Cells

        while True:
            neighbors = self._get_unvisited_neighbors(x, y, maze)

            if neighbors:
                neighbor = random.choice(neighbors)
                maze[neighbor["y"]][neighbor["x"]].visited = True
                (maze[neighbor["y"]][neighbor["x"]]
                 .walls[neighbor["neighbors_direction"]]) = False
                maze[y][x].walls[neighbor["current_cell_direction"]] = False

                stack.append((x, y))
                x, y = neighbor["x"], neighbor["y"]
            elif stack:
                x, y = stack.pop()
            else:
                break

        if not self.perfect:
            walls_num = (self.height * self.width) // 10
            maze = self._remove_random_walls(maze, walls_num)
            # self.print_maze(maze)
        maze_integer = self._cells_to_integers(maze)
        return maze_integer

    def save_maze(self, maze, filename):
        with open(filename, "w", encoding="utf-8") as file:
            for y in range(self.height):
                line = ''
                for x in range(self.width):
                    value = 0
                    if maze[y][x].walls["north"]:
                        value = value | 1
                    if maze[y][x].walls["east"]:
                        value = value | 2
                    if maze[y][x].walls["south"]:
                        value = value | 4
                    if maze[y][x].walls["west"]:
                        value = value | 8
                    line += format(value, "X")
                file.write(line)
                if y != self.height - 1:
                    file.write('\n')


# if __name__ == "__main__":
#     try:
#         # If executed as a package (python -m), relative import works
#         from ..config_parser import config_parser
#     except (ImportError, ValueError):
#         # If executed as a script,
#         # add parent folder to sys.path and import absolutely
#         import os
#         import sys

#         ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#         if ROOT not in sys.path:
#             sys.path.insert(0, ROOT)
#         from config_parser import config_parser

#     config = config_parser("/home/dvasilev/Documents/"
#                            "core/Milestone2/amazing/config.txt")
#     print(config)

#     gen = MazeGenerator(config)
#     try:
#         gen = MazeGenerator(config)
#         maze = gen.generate()

#         print(maze)

#     except Exception as e:
#         print(e)
