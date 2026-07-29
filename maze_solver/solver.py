from collections import deque
from typing import List, Tuple, Optional, Dict


def get_neighbors(maze: List[List[int]],
                  cell: Tuple[int, int]
                  ) -> List[Tuple[int, int]]:
    neighbors: List[Tuple[int, int]] = []
    x, y = cell
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    total_rows = len(maze)
    total_cols = len(maze[0]) if total_rows > 0 else 0
    for dx, dy in directions:
        nx = x + dx
        ny = y + dy
        if 0 <= nx < total_cols and 0 <= ny < total_rows:
            neighbors.append((nx, ny))
    return neighbors


direction_masks = {
    (0, -1): 1,
    (1, 0): 2,
    (0, 1): 4,
    (-1, 0): 8
}

opposite_masks = {
    1: 4,
    2: 8,
    4: 1,
    8: 2
}


def is_walkable(maze: List[List[int]],
                cell: Tuple[int, int],
                neighbor_cell: Tuple[int, int]) -> bool:
    curr_x, curr_y = cell
    nghbr_x, nghbr_y = neighbor_cell
    change = (nghbr_x - curr_x, nghbr_y - curr_y)
    if change not in direction_masks:
        return False
    out_wall = direction_masks[change]
    in_wall = opposite_masks[out_wall]
    if (maze[curr_y][curr_x] & out_wall) != 0:
        return False
    if (maze[nghbr_y][nghbr_x] & in_wall) != 0:
        return False
    return True


def solve_maze(
        maze: List[List[int]],
        start: Tuple[int, int],
        exit: Tuple[int, int]
        ) -> Optional[List[Tuple[int, int]] | None]:
    queue = deque([start])
    visited = {start}
    parent_map: Dict[Tuple[int, int], Tuple[int, int] | None] = {start: None}

    while queue:
        current: Tuple[int, int] | None = queue.popleft()  # TODOOOO
        if current == exit:
            path = []
            while current is not None:
                path.append(current)
                current = parent_map[current]
            path.reverse()
            return path
        if current is not None:
            for nghbor in get_neighbors(maze, current):
                if nghbor not in visited \
                          and is_walkable(maze, current, nghbor):
                    visited.add(nghbor)
                    parent_map[nghbor] = current
                    queue.append(nghbor)
    return None
