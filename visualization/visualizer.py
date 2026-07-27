#!/usr/bin/env python3

import time

COLOR_MAP = {
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "blue": "\x1b[34m",
    "yellow": "\x1b[33m",
    "reset": "\x1b[0m"
}


def print_maze(maze, path, config, show_path=True, wall_color=None):
    color_code = COLOR_MAP.get(wall_color, "") if wall_color else ""
    reset_code = COLOR_MAP["reset"] if color_code else ""

    def w(char):
        return f"{color_code}{char}{reset_code}" if color_code else char

    # Top border
    print(w("+") + w("---+") * config["WIDTH"])

    for y in range(config["HEIGHT"]):
        # vertical walls
        line = w("|")
        for x in range(config["WIDTH"]):
            # entry coordinates
            if ((x, y) == config["ENTRY"]):
                line += '\x1b[32m█S█\x1b[0m'
            elif ((x, y) == config["EXIT"]):
                line += '\x1b[35m█E█\x1b[0m'
            elif path and ((x, y) in path) and show_path:
                line += '\x1b[38;5;229m███\x1b[0m'
            elif maze[y][x] == 15:  # 42 pattern
                line += '\x1b[38;5;45m███\x1b[0m'
            else:
                line += "   "
            if maze[y][x] in [2, 3, 6, 7, 10, 11, 14, 15]:  # east wall closed
                line += w("|")
            else:
                line += " "
        print(line)

        # horizontal walls
        line = w("+")
        for x in range(config["WIDTH"]):
            if maze[y][x] in [4, 5, 6, 7, 12, 13, 14, 15]:  # south wall closed
                line += w("---+")
            else:
                line += "   " + w("+")
        print(line)


def animate_path(maze, full_path, config, wall_color=None, delay=0.08):
    if not full_path:
        return
    for i in range(1, len(full_path) + 1):
        print("\033[H\033[J", end="")
        partial_path = full_path[:i]
        print_maze(maze, partial_path, config, show_path=True,
                   wall_color=wall_color)
        time.sleep(delay)
