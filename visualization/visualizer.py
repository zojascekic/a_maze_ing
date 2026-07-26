#!/usr/bin/env python3

def print_maze(maze, path, config, show_path=True, wall_color=None):
    # Top border
    print("+" + "---+" * config["WIDTH"])

    for y in range(config["HEIGHT"]):
        # vertical walls
        line = "|"
        for x in range(config["WIDTH"]):
            # entry coordinates
            if ((x, y) == config["ENTRY"]):
                line += '\x1b[32m█S█\x1b[0m'
            elif ((x, y) == config["EXIT"]):
                line += '\x1b[35m█E█\x1b[0m'
            elif path and ((x, y) in path) and show_path:
                line += '\x1b[36m███\x1b[0m'
            elif maze[y][x] == 15:  # 42 pattern
                line += '\x1b[93m███\x1b[0m'
            else:
                line += "   "
            if maze[y][x] in [2, 3, 6, 7, 10, 11, 14, 15]:  # east wall closed
                line += "|"
            else:
                line += " "
        print(line)

        # horizontal walls
        line = "+"
        for x in range(config["WIDTH"]):
            if maze[y][x] in [4, 5, 6, 7, 12, 13, 14, 15]:  # south wall closed
                line += "---+"
            else:
                line += "   +"
        print(line)
