from queue import Queue

def parse_input(filepath: str) -> list[list[str]]:
    result = []
    with open(filepath, 'r') as file:
        for line in file:
            result.append(list(line.rstrip('\n')))
    return result

def rotate_dir_90(dir: tuple[int, int]) -> tuple[int, int]:
    # Rotates the direction 90 degrees to the right
    return (dir[1], -dir[0])

def count_steps(grid: list[list[str]]) -> int:
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
    # Use BFS to traverse the map
    while q.qsize() > 0:
        pos, dir = q.get()
        grid[pos[0]][pos[1]] = 'X'
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

if __name__ == "__main__":
    grid = parse_input("day_6/input.txt")
    num_steps = count_steps(grid)
    print(f"num_steps: {num_steps}")
