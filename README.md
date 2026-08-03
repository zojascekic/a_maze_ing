*This project has been created as part of the 42 curriculum by dvasilev and zscekic.*

# A-maze-ing

**A-Maze-ing** is a Python application designed to generate, encode, and visually represent mazes. Given a configuration file specifying maze dimensions and properties, the program creates a maze (such as a perfect maze with a single unique path between entrance and exit), calculates the shortest solution path, and displays the maze interactively. 

*Key capabilities of the project include:*

- **Algorithmic Maze Generation:** Programmatically builds mazes based on graph theory and algorithmic generation techniques.

- **Interactive Visualization:** Displays the generated maze using terminal-based ASCII graphics or a GUI, complete with features to toggle solution paths and customize color themes.

- **Data Encoding & Export:** Formats and outputs the generated maze structure into a standardized hexadecimal wall representation along with entry/exit coordinates and path steps.

- **Reusable Architecture:** Distributes the core maze generation logic as an independent Python package (`mazegen`) for seamless integration into future projects.

## Detailed description

### 📄 Configuration File Structure & Format

The application parses a plain text configuration file to parameterize maze generation. The configuration file follows a simple key-value format (or structured text) specifying all necessary constraints:

- **Dimensions:** `WIDTH` and `HEIGHT` of the maze grid.
- **Coordinates:** `ENTRY` and `EXIT` positions defined as `(x, y)` coordinates within bounds.
- **Generation Parameters:**
  - `PERFECT` (boolean / flag): Dictates whether to build a perfect maze (exactly one unique path between any two points) or allow loops.
  - `SEED` (optional integer): Ensures deterministic generation for testing and reproducibility.
- **Output File Path:** `OUTPUT_FILE` specifying where to export the generated hexadecimal matrix.

---

### 🎲 Maze Generation — Chosen Algorithm & Justification

* **Algorithm Used:** **Iterative Backtracker (Randomized Depth-First Search)**.
* **Why this Algorithm?**
  * **Spanning Tree Guarantee:** A DFS-based spanning tree guarantees 100% connectivity across all non-blocked cells. When `PERFECT` mode is enabled, it ensures a **perfect maze** with no isolated loops and exactly one solution path.
  * **Long & Winding Corridors:** DFS generates mazes with long, winding paths and low branching factors, making the maze visually appealing and challenging to solve.
  * **Customizable Loops & Constraints:** Easily supports post-processing steps—such as removing extra walls when `PERFECT=False` to introduce loops while preserving structural constraints (e.g., preventing open 3x3 areas).
  * **Efficiency:** Runs in $\mathcal{O}(V + E)$ time complexity and $\mathcal{O}(V)$ space complexity using an explicit stack, making it lightweight and fast for large grid dimensions.

---

### 🧩 Maze Solving — Chosen Algorithm & Justification

* **Algorithm Used:** **Breadth-First Search (BFS)**
* **Why this Algorithm?**
  * **Shortest Path Guarantee:** BFS explores all nodes level-by-level, guaranteeing the **absolute shortest path** from entry to exit in unweighted grid graphs.
  * **Unreachable Traversal Handling:** Safely detects unsolvable mazes (or unreachable coordinates) and returns `None` without getting stuck in infinite recursion loops.
  * **Deterministic Path Retrieval:** Parent pointer tracking allows simple back-tracing from the exit coordinate back to the entry point to produce an ordered solution path list `[(x1, y1), (x2, y2), ...]`.

---

### 🎨 Visual Representation & Terminal Rendering

The project features a lightweight, ANSI-powered terminal renderer that transforms the integer wall bitmask matrix into a crisp 2D visual layout directly in your console.

## 🧱 ASCII Grid Construction

Because standard terminal characters cannot combine cell centers and outer walls into a single character space, the grid is rendered row-by-row using a structured block layout:

* **Top Border:** Renders an initial outer boundary (`+---+...`).
* **Cell Content & Vertical Walls (`line 1`):**
  * **Start Point (`S`):** Highlighted with a green block (`\x1b[32m█S█\x1b[0m`).
  * **Exit Point (`E`):** Highlighted with a magenta block (`\x1b[35m█E█\x1b[0m`).
  * **Solution Path:** Displayed with warm yellow blocks (`\x1b[38;5;229m███\x1b[0m`).
  * **Embedded '42' Pattern:** Highlighted with bright cyan blocks (`\x1b[38;5;45m███\x1b[0m`) for fully enclosed cells (bitmask `15`).
  * **East Walls:** Evaluated via bitwise inspection (`[2, 3, 6, 7, 10, 11, 14, 15]`) to print dynamic vertical dividers (`|`).
* **Horizontal Passages (`line 2`):**
  * **South Walls:** Evaluated via bitwise inspection (`[4, 5, 6, 7, 12, 13, 14, 15]`) to render lower cell borders (`---+`) or open floor gaps (`   +`).

---

### 🌈 ANSI Customization & Color Support

The rendering engine includes configurable themes via a built-in `COLOR_MAP`:

* **Dynamic Wall Themes:** Maze walls can be colored in `red`, `green`, `blue`, or `yellow` using ANSI color escape codes while keeping path markers distinct.
* **Toggleable Path:** The solution path display can be toggled on or off programmatically (`show_path=True/False`).

---

### 🎬 Real-Time Path Animation

The renderer includes a step-by-step path animation engine (`animate_path`):

* **Frame-by-Frame Drawing:** Sequentially slice-renders path coordinates from start to end (`full_path[:i]`).
* **Terminal Clearing:** Uses the `\033[H\033[J` ANSI escape sequence to reset the cursor to the top-left and clear the screen between frames for smooth, flicker-free rendering.
* **Configurable Speed:** Supports continuous path progression controlled by a customizable time delay (defaulting to `0.08s` per step).

## Instructions

```
make install
make run
```

## 👥 Team & Contributions

This project was developed collaboratively by **Diana (dvasilev)** and **Zoja (zscekic)**. From the outset, we established a clear execution plan and stuck to it from beginning to end, ensuring steady progress and an efficient development process.

---

### 🎭 Roles & Responsibilities

| Team Member | Core Responsibilities & Contributions |
| :--- | :--- |
| **dvasilev** | • Designed and implemented the **Maze Generation** logic (Iterative Backtracker DFS, 3x3 hall prevention, and '42' pattern embedding).<br>• Structured data handling and conversion for **Hexadecimal/Bitmask** output.<br>• Co-developed the **Terminal Visualizer** engine. |
| **zscekic** | • Developed the **Maze Solver** module (Shortest-path search & path reconstruction).<br>• Built the **Configuration Parser** to validate and load parameters safely.<br>• Set up the **Virtual Environment (`venv`)**, package structure, and project build.<br>• Authored the complete project **`README.md`** documentation.<br>• Co-developed the **Terminal Visualizer** engine. |

---

### 🗺️ Planning & Evolving

We kicked off the project by breaking down the 42 subject requirements into distinct modular components. By defining strict module interfaces early on (e.g., how `MazeConfig` passes data to `MazeGenerator` and how solver paths feed into the visualizer), both team members were able to build and test their respective modules independently without blocking each other.

---

### ✨ What Worked Well

* **Adherence to Plan:** Staying aligned with our original design schedule prevented feature creep and kept development focused on core criteria.
* **Balanced Workload:** Dividing backend generation, pathfinding algorithms, environment setup, and visual tools equally allowed both of us to take full ownership of key architecture parts while pairing up on complex components like terminal rendering.
* **Seamless Integration:** Because data structures were agreed upon upfront, integrating generation, solving, and output encoding went smoothly without major refactoring.

---

### 🛠️ Tools & Collaboration

* **Trello:** Used as our primary Kanban board for task assignment, milestone tracking, and progress management.
* **Git & GitHub:** Used for structured feature branching, pull requests, and peer code reviews to maintain code quality.

## Resources
The following references were useful for understanding and implementing the functions in this project:
- https://en.wikipedia.org/wiki/Breadth-first_search
- https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/
- https://www.w3schools.com/python/python_virtualenv.asp
- https://peps.python.org/pep-0257/
- https://dev.to/dev_neil_a/python-how-to-adding-color-and-styles-to-terminal-text-3699
- https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
- https://aryanab.medium.com/maze-generation-recursive-backtracking-5981bc5cc766

#### AI usage
ChatGPT and Gemini was used for:

- Teamwork planning
- Understanding algorithms
- Understanding implementation approaches
- Clarifying Python language concepts
- Debugging
- Readme file generation