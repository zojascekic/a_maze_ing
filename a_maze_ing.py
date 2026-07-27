#!/usr/bin/env python3

from config_parser import config_parser
from maze_generator.generator import MazeGenerator
from maze_solver.solver import solve_maze
from visualization.visualizer import print_maze, animate_path
import random
import subprocess
import os

if __name__ == "__main__":

    # try:
    #     config = config_parser("config.txt")
    #     print(config)
    #     gen = MazeGenerator(config)
    #     maze = gen.generate()
    #     print(maze)

    #     start = (0, 0)
    #     exit_cell = (0, 2)
    #     path = solve_maze(maze, start, exit_cell)
    # except Exception as e:
    #     print(e)

    config = config_parser("config.txt")

    gen = MazeGenerator(config)
    maze = gen.generate()

    start = config["ENTRY"]
    exit_cell = config["EXIT"]
    path = solve_maze(maze, start, exit_cell)
    path_showed = False
    color = None

    def clear_screen():
        cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run(cmd, shell=True)

    while True:
        clear_screen()
        print_maze(maze, path, config, show_path=path_showed, wall_color=color)

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
            print_maze(maze, None, config, show_path=False, wall_color=color)
        elif user_input == 'c':
            print("Changing wall color...")
            chosen_color = input("Enter a new wall "
                                 "color (avalible colors: "
                                 "red, green, blue, yellow): ").strip().lower()
            if chosen_color in ["red", "green", "blue", "yellow"]:
                color = chosen_color
            else:
                print("You entered invalid color... "
                      "Choose red, green, blue or yellow")
                continue
            print_maze(maze, path, config,
                       show_path=path_showed, wall_color=color)
        else:
            print("Invalid input. Please try again.")
            continue
