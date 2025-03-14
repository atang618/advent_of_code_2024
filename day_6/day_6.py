from queue import Queue
import copy
from typing import Optional
from tqdm import tqdm

def parse_input(filepath: str) -> list[list[str]]:
    result = []
    with open(filepath, 'r') as file:
        for line in file:
            result.append(list(line.rstrip('\n')))
    return result

def rotate_dir_90(dir: tuple[int, int]) -> tuple[int, int]:
    # Rotates the direction 90 degrees to the right
    return (dir[1], -dir[0])

def count_steps(input_grid: list[list[str]]) -> Optional[int]:
    '''
    Counts the number of distinct steps to get out of the grid.
    Returns None if infinite loop detected.
    '''
    grid = copy.deepcopy(input_grid)
    m = len(grid)
    if m == 0:
        return 0
    n = len(grid[0])

    def in_bounds(x: int, y: int) -> bool:
        return 0 <= x < m and 0 <= y < n

    # Find the start position
    q = Queue()
    start_dir = (-1, 0)
    for i, line in enumerate(grid):
        for j, ch in enumerate(line):
            if ch == '^':
                q.put(((i, j), start_dir))
    visited = set()
    # Use BFS to traverse the map
    while q.qsize() > 0:
        pos, dir = q.get()
        grid[pos[0]][pos[1]] = 'X'
        state = (pos, dir)
        if state in visited:
            return None
        visited.add(state)
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if not in_bounds(next_pos[0], next_pos[1]):
            # print(f"exited: {pos}, {dir}")
            break
        if grid[next_pos[0]][next_pos[1]] == '#':
            q.put((pos, rotate_dir_90(dir)))
        else:
            q.put((next_pos, dir))

    # Count Xs
    steps = 0
    for line in grid:
        for ch in line:
            if ch == 'X':
                steps += 1
    
    return steps

# Warning: this currently undercounts the possibilities significantly
def count_obs(input_grid: list[list[str]]) -> int:
    grid = copy.deepcopy(input_grid)
    m = len(grid)
    if m == 0:
        return 0
    n = len(grid[0])

    def in_bounds(pos: tuple[int, int]) -> bool:
        x, y = pos
        return 0 <= x < m and 0 <= y < n

    def get_possible_state(pos: tuple[int, int], dir: tuple[int, int]):
        next_pos = pos
        while in_bounds(next_pos) and grid[next_pos[0]][next_pos[1]] != '#':
            yield (next_pos, dir)
            next_pos = tuple(map(sum, zip(next_pos, dir)))

    # Find the start position
    q = Queue()
    start_pos = (0, 0)
    start_dir = (-1, 0)
    visited = set()
    for i, line in enumerate(grid):
        for j, ch in enumerate(line):
            if ch == '^':
                start_pos = (i, j)
                q.put((start_pos, start_dir))
                
    # Use BFS to traverse the map
    num_obs = 0
    while q.qsize() > 0:
        pos, dir = q.get()
        state = (pos, dir)
        visited.add(state)
        grid[pos[0]][pos[1]] = 'X'
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if not in_bounds(next_pos):
            break
        rot_dir = rotate_dir_90(dir)
        if grid[next_pos[0]][next_pos[1]] == '#':
            q.put((pos, rot_dir))
        elif grid[next_pos[0]][next_pos[1]] == 'X':
            # Can't put obstacle where the guard already walked
            q.put((next_pos, dir))
        else:
            # Check if we could get into an infinite loop with rotation
            for state in get_possible_state(pos, rot_dir):
                if state in visited:
                    num_obs += 1
                    break
            q.put((next_pos, dir))

    return num_obs

def count_obs_brute_force(grid: list[list[str]]) -> int:
    # Place an obstacle at each location and check if we get infinite loop
    num_obs = 0
    for i, line in enumerate(tqdm(grid, desc="Rows")):
        for j, c in enumerate(tqdm(line, desc="Columns", leave=False)):
            if c != '.':
                continue
            grid[i][j] = '#'
            if count_steps(grid) is None:
                num_obs += 1
            grid[i][j] = '.'

    return num_obs

if __name__ == "__main__":
    grid = parse_input("day_6/input.txt")
    num_steps = count_steps(grid)
    print(f"num_steps: {num_steps}")
    num_obs = count_obs_brute_force(grid)
    print(f"num_obs: {num_obs}")
