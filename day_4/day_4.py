from queue import Queue
import operator

def read_input(filepath: str) -> list[str]:
    result = []
    with open(filepath, 'r') as file:
        for line in file:
            result.append(line.rstrip('\n'))
    return result


def find_xmas(grid: list[str], target: str = "XMAS", cross_only: bool = False) -> int:
    m = len(grid)
    if m == 0:
        return 0
    n = len(grid[0])
    q = Queue()

    def in_bounds(x: int, y: int) -> bool:
        return 0 <= x < m and 0 <= y < n
    
    def get_directions(x: int, y: int):
        axis_dir = [-1, 0, 1] 
        if cross_only:
            axis_dir.remove(0)
        for dx in axis_dir:
            for dy in axis_dir:
                if dx == 0 and dy == 0:
                    continue
                x_1 = x + dx
                y_1 = y + dy
                if in_bounds(x_1, y_1):
                    yield dx, dy

    for i in range(m):
        for j in range(n):
            if grid[i][j] == target[0]:
                for dx, dy in get_directions(i, j):
                    q.put((1, (i + dx, j + dy), (dx, dy)))
    count = 0
    visited_coords = set()
    while q.qsize() > 0:
        idx, coord, dir = q.get()
        ch = grid[coord[0]][coord[1]]
        if ch != target[idx]:
            continue
        if idx == len(target) - 1:
            if not cross_only:
                count += 1
            else:
                prev_coord =tuple(map(operator.sub, coord, dir))
                if prev_coord in visited_coords:
                    count += 1
                    # print(f"{prev_coord}")
                    visited_coords.remove(prev_coord)
                else:
                    visited_coords.add(prev_coord)
        else:
            x1 = coord[0] + dir[0]
            y1 = coord[1] + dir[1]
            if in_bounds(x1, y1):
                q.put((idx + 1, (x1, y1), dir))

    return count

if __name__ == "__main__":
    grid = read_input("day_4/input.txt")
    num_xmas = find_xmas(grid)
    print(f"num_xmas: {num_xmas}")
    num_x_mas = find_xmas(grid, "MAS", True)
    print(f"num_x_mas: {num_x_mas}")
