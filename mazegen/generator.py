import random
from typing import List, Dict, Any, cast, TypedDict, Tuple, Optional
import os


class MazeConfig(TypedDict):
    """Represent the structural configuration schema for maze generation.
        Attributes:
            WIDTH (int): Horizontal dimension of the maze grid.
            HEIGHT (int): Vertical dimension of the maze grid.
            ENTRY (Tuple[int, int]): Starting grid coordinates as (x, y).
            EXIT (Tuple[int, int]): Ending grid coordinates as (x, y).
            PERFECT (bool): Flag indicating if the maze is loop-free.
            OUTPUT_FILE (str): Target filepath for saving generated maze.
            SEED (Optional[int]): Random seed for deterministic generation.
        """
    WIDTH: int
    HEIGHT: int
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    PERFECT: bool
    OUTPUT_FILE: str
    SEED: Optional[int]


def config_parser(filepath: str) -> MazeConfig:
    """Parse, validate, and convert a key-value maze configuration file.

    Args:
        filepath (str): Path to the key-value configuration text file.

    Returns:
        MazeConfig: A strongly-typed dictionary containing validated settings.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If file syntax is invalid, required keys are missing,
            types cannot be converted, or coordinate values are out of bounds.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: file with filepath"
                                f"{filepath} not found!")

    config_dict: Dict[str, str] = {}
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError("Invalid syntax for config file, missing =")
            key, val = line.split("=")
            config_dict[key.strip().upper()] = val.strip()
        key_list = ["WIDTH", "HEIGHT", "ENTRY",
                    "EXIT", "PERFECT", "OUTPUT_FILE"]
        missing_keys = []
        for key in key_list:
            if key not in config_dict.keys():
                missing_keys.append(key)
        if missing_keys:
            missing_keys_str = ",".join(missing_keys)
            raise ValueError(f"Invalid syntax for config file:"
                             f"missing keys [{missing_keys_str}]")
        try:
            width = int(config_dict["WIDTH"])
            height = int(config_dict["HEIGHT"])
        except ValueError:
            raise ValueError("Width and height have to be integers")

        seed: Optional[int] = None
        if "SEED" in config_dict:
            try:
                seed = int(config_dict["SEED"])
            except ValueError:
                raise ValueError("SEED has to be an integer")

        try:
            entry_str = config_dict["ENTRY"].split(',')
            if len(entry_str) != 2:
                raise ValueError("ENTRY must be formatted as 'x,y'")
            entry_coords = (int(entry_str[0]), int(entry_str[1]))
            exit_str = config_dict["EXIT"].split(',')
            if len(exit_str) != 2:
                raise ValueError("EXIT must be formatted as 'x,y'")
            exit_coords = (int(exit_str[0]), int(exit_str[1]))
            val = config_dict["PERFECT"].lower()
            if val in ("true", "1", "yes"):
                perfect = True
            elif val in ("false", "0", "no"):
                perfect = False
            else:
                raise ValueError("PERFECT must be True or False")
            output_file = config_dict["OUTPUT_FILE"].strip()
            if not output_file:
                raise ValueError("Output file cannot be empty")
            if os.path.isdir(output_file):
                raise ValueError("Provided output file is a directory, "
                                 "it must be a file")
            parent_dir = os.path.dirname(output_file) or "."
            if not os.path.exists(parent_dir):
                raise ValueError(f"Destination directory '{parent_dir}'"
                                 f"does not exist")
        except ValueError as e:
            raise ValueError(f"Invalid syntax for config file: {e}")
        if width < 0 or height < 0:
            raise ValueError("Width and height values have to be positive")
        if entry_coords[0] < 0 or entry_coords[0] >= width:
            raise ValueError("Entry coordinate out of boundaries")
        if entry_coords[1] < 0 or entry_coords[1] >= height:
            raise ValueError("Entry coordinate out of boundaries")
        if exit_coords[0] < 0 or exit_coords[0] >= width:
            raise ValueError("Exit coordinate out of boundaries")
        if exit_coords[1] < 0 or exit_coords[1] >= height:
            raise ValueError("Exit coordinate out of boundaries")
        if entry_coords == exit_coords:
            raise ValueError("Entry and Exit coordinates cannot be the same")
    return {
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry_coords,
        "EXIT": exit_coords,
        "PERFECT": perfect,
        "OUTPUT_FILE": output_file,
        "SEED": seed
        }


class Cell():
    """Represent a single grid cell within a maze.

    Attributes:
        visited (bool): Indicates whether the cell has been
                        processed during generation.
        blocked (bool): Indicates if the cell is blocked for
                        custom structural patterns.
        walls (dict[str, bool]): Status of the four surrounding
                                walls (north, east, south, west).
    """
    def __init__(self) -> None:
        self.visited = False
        self.blocked = False  # for 42 pattern
        self.walls = {
            "north": True,
            "east": True,
            "south": True,
            "west": True
        }


class MazeGenerator():
    """Generate 2D grid mazes with configurable dimensions,
       patterns, and wall properties.

    Attributes:
        seed (int | None): Seed value used for deterministic random generation.
        width (int): Horizontal cell count of the maze grid.
        height (int): Vertical cell count of the maze grid.
        perfect (bool): Indicating if the maze should have only one solution.
        entry (Tuple[int, int]): Grid coordinates for the maze entry point.
        exit (Tuple[int, int]): Grid coordinates for the maze exit point.
    """
    def __init__(self, config_path: str) -> None:
        """Initialize generator instance attributes from config file.

        Args:
            config (MazeConfig): Object containing maze parameter values.
        """
        config = config_parser(config_path)
        self.seed = config["SEED"]
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.perfect = config["PERFECT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.output_file = config["OUTPUT_FILE"]

    def _set_42_pattern(self, maze: List[List[Cell]]) -> List[List[Cell]]:
        """Embed a blocked numerical "42" shape into the grid layout.

        Args:
            maze (List[List[Cell]]): Grid matrix of Cell instances.

        Returns:
            List[List[Cell]]: Updated grid matrix with designated
            cells set as blocked.
        """
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

    def _get_starting_point(self, maze: List[List[Cell]]) -> List[List[int]]:
        """Retrieve all grid coordinates that are not marked as blocked.

        Args:
            maze (List[List[Cell]]): Grid matrix of Cell instances.

        Returns:
            List[List[int]]: Collection of available coordinate pairs [x, y].
        """
        non_blocked_sells = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                if not maze[y][x].blocked:
                    non_blocked_sells.append([x, y])
        return non_blocked_sells

    def _get_unvisited_neighbors(self, x: int, y: int, maze: List[List[Cell]]
                                 ) -> List[Dict[str, Any]]:
        """Find adjacent cells that have not been visited and are not blocked.

        Args:
            x (int): Horizontal coordinate of the current cell.
            y (int): Vertical coordinate of the current cell.
            maze (List[List[Cell]]): Grid matrix of Cell instances.

        Returns:
            List[Dict[str, Any]]: Metadata dicts for each
            eligible neighboring cell.
        """
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

    def has_open_3x3(self, maze: List[List[Cell]], x: int, y: int) -> bool:
        """Check whether removing walls forms a completely open 3x3 section.

        Args:
            maze (List[List[Cell]]): Grid matrix of Cell instances.
            x (int): Horizontal coordinate of the target cell.
            y (int): Vertical coordinate of the target cell.

        Returns:
            bool: True if an open 3x3 area overlaps the cell, False otherwise.
        """
        def is_open_3x3(maze: List[List[Cell]], x: int, y: int) -> bool:
            """Determine if a specific 3x3 window starting at (x, y)
               has no internal walls.

            Args:
                maze (List[List[Cell]]): Grid matrix of Cell instances.
                x (int): Top-left horizontal coordinate of the 3x3 window.
                y (int): Top-left vertical coordinate of the 3x3 window.

            Returns:
                bool: True if all inner walls are absent, False otherwise.
            """
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

    def _remove_random_walls(self, maze: List[List[Cell]], walls_num: int
                             ) -> List[List[Cell]]:
        """Remove additional walls at random to introduce
        loops without creating 3x3 halls.

        Args:
            maze (List[List[Cell]]): Grid matrix of Cell instances.
            walls_num (int): Target count of interior walls to remove.

        Returns:
            List[List[Cell]]: Modified grid matrix containing extra passages.
        """
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
            nx = cast(int, neighbor["x"])
            ny = cast(int, neighbor["y"])
            c_dir: str = str(neighbor["current_cell_direction"])
            n_dir: str = str(neighbor["neighbors_direction"])
            if maze[ny][nx].blocked:
                continue
            if maze[y][x].walls[c_dir]:
                maze[y][x].walls[c_dir] = False
                (maze[ny][nx]
                 .walls[n_dir]) = False
                if self.has_open_3x3(maze, x, y) or \
                   self.has_open_3x3(maze, nx, ny):
                    maze[y][x].walls[c_dir] = True
                    (maze[ny][nx]
                     .walls[n_dir]) = True
                    count_3x3_open_areas += 1
                else:
                    removed += 1
        return maze

    def _cells_to_integers(self, maze: List[List[Cell]]) -> List[List[int]]:
        """Convert Cell objects into bitmask integers
        representing wall configurations.

        Args:
            maze (List[List[Cell]]): Grid matrix of Cell instances.

        Returns:
            List[List[int]]: Bitmask integer
            matrix encoding wall presence per cell.
        """
        maze_integer: List[List[int]] = [[] * self.width] * self.height
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

    def generate(self, seed: int | None = None) -> list[list[int]]:
        """Execute the maze generation algorithm and return a
        bitmask matrix representation.

        Args:
            seed (int | None, optional): Override seed for
            the random number generator.

        Returns:
            list[list[int]]: Two-dimensional matrix of integer wall bitmasks.

        Raises:
            ValueError: If entry or exit coordinates
            overlap with the "42" pattern.
        """
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
            neighbors: List[Dict[str, Any]
                            ] = self._get_unvisited_neighbors(x, y, maze)

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
        maze_integer = self._cells_to_integers(maze)
        return maze_integer
