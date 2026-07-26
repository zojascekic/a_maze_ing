#!/usr/bin/env python3

from config_parser import config_parser
from maze_generator.generator import MazeGenerator
from maze_solver.solver import solve_maze
from visualization.visualizer import print_maze
import random


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
    print_maze(maze, path, config, show_path=False)

    # print(maze)
    # print(path)
    while True:
        user_input = input("\nOptions: \nregenerate maze: r \nshow path: s \nhide path: h \nchange wall color: c \nquit: q\n").lower().strip()

        if user_input == 'q':
            print("Goodbye!")
            break
        elif user_input == 'r':
            print("Regenerating maze...")
            maze = gen.generate(random.randint(0, 10000))  # gen new maze +r sd
            path = solve_maze(maze, start, exit_cell)
            print_maze(maze, path, config, show_path=False)
        elif user_input == 's':
            print("Showing path...")
            print_maze(maze, path, config, show_path=True)
        elif user_input == 'h':
            print("Hiding path...")
            print_maze(maze, None, config, show_path=False)
        elif user_input == 'c':
            print("Changing wall color...")
            print_maze(maze, path, config, show_path=True,
                       wall_color=input("Enter a new wall color (avalible \
                                        colors: red, green, \
                                        blue, orange): ").strip())
        else:
            print("Invalid input. Please try again.")

        # TODO change maze wall colors:
        # line 52 (now it does nothing, but it should change the
        # wall color of the maze based on user input)
