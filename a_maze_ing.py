#!/usr/bin/env python3

from config_parser import config_parser
from maze_generator.generator import MazeGenerator
from maze_solver.solver import solve_maze
from visualization.visualizer import print_maze, animate_path
import random
import subprocess
import os

if __name__ == "__main__":
    try:
        config = config_parser("config.txt")

        gen = MazeGenerator(config)
        maze = gen.generate()
        start = config["ENTRY"]
        exit_cell = config["EXIT"]
        path = solve_maze(maze, start, exit_cell)
        path_showed = False
        color = None

        def path_to_directions(path):
            directions = []
            for i in range(len(path) - 1):
                x1, y1 = path[i]
                x2, y2 = path[i + 1]

                dx = x2 - x1
                dy = y2 - y1

                if dx == 1:
                    directions.append("E")
                elif dx == -1:
                    directions.append("W")
                elif dy == 1:
                    directions.append("S")
                elif dy == -1:
                    directions.append("N")

            return "".join(directions)

        def save_maze(maze, filename):
            with open(filename, "w", encoding="utf-8") as file:
                for y in range(config["HEIGHT"]):
                    for x in range(config["WIDTH"]):
                        line = ''
                        line += format(maze[y][x], "X")
                        file.write(line)
                    file.write('\n')
                file.write('\n' + ",".join(map(str, start)) + '\n')
                file.write(",".join(map(str, exit_cell)) + '\n')
                file.write(path_to_directions(path))

        save_maze(maze, config["OUTPUT_FILE"])

        def clear_screen():
            cmd = 'cls' if os.name == 'nt' else 'clear'
            subprocess.run(cmd, shell=True)

        while True:
            clear_screen()
            print_maze(maze, path, config, show_path=path_showed,
                       wall_color=color)
            print(path)

            user_input = input(
                "\n\x1b[1;3;37;46m Options \x1b[0m\n"
                "  \x1b[3;36mregenerate maze:\x1b[0m \x1b[1;36mr\x1b[0m\n"
                "  \x1b[3;32mshow path:\x1b[0m \x1b[1;32ms\x1b[0m\n"
                "  \x1b[3;33mhide path:\x1b[0m \x1b[1;33mh\x1b[0m\n"
                "  \x1b[3;35mchange wall color:\x1b[0m \x1b[1;35mc\x1b[0m\n"
                "  \x1b[3;31mquit:\x1b[0m \x1b[1;31mq\x1b[0m\n> "
            ).lower().strip()

            if user_input == 'q':
                print("\x1b[1;32;40mGoodbye!\x1b[0m")
                break
            elif user_input == 'r':
                print("Regenerating maze...")
                maze = gen.generate(random.randint(0, 10000))  # gen with rseed
                # maze = gen.generate(random.seed(config[SEED]))
                # # gen with rseed
                path = solve_maze(maze, start, exit_cell)
                path_showed = False
                print_maze(maze, path, config, show_path=path_showed,
                           wall_color=color)
            elif user_input == 's':
                print("Showing path...")
                animate_path(maze, path, config, wall_color=color)
                path_showed = True
            elif user_input == 'h':
                print("Hiding path...")
                path_showed = False
                print_maze(maze, None, config,
                           show_path=False, wall_color=color)
            elif user_input == 'c':
                print("Changing wall color...")
                chosen_color = input("Enter a new wall "
                                     "color (avalible colors: "
                                     "red, green, blue, yellow): "
                                     ).strip().lower()
                if chosen_color in ["red", "green", "blue", "yellow"]:
                    color = chosen_color
                else:
                    print("You entered invalid color... "
                          "Choose red, green, blue or yellow")
                    continue
                print_maze(maze, path, config,
                           show_path=path_showed, wall_color=color)
            else:
                while input("Invalid input. Press Enter to try again... "
                            ).strip() != "":
                    pass
                continue
    except Exception as e:
        print(f"\n\x1b[1;31mAn unexpected error occurred:\x1b[0m {e}")
