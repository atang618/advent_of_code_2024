from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

def parse_input(filepath: str) -> list[list[str]]:
    result = []
    with open(filepath, 'r') as file:
        for line in file:
            result.append(list(line.rstrip('\n')))
    return result

@dataclass
class Vector:
    dx: int
    dy: int

@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __sub__(self, other: 'Point') -> Vector:
        return Vector(dx=self.x-other.x, dy=self.y-other.y)
    
    def __add__(self, other) -> 'Point':
        if isinstance(other, Vector):
            return Point(x=self.x + other.dx, y=self.y + other.dy)
        raise NotImplementedError(f"add not supported between Point and {type(other).__name__}")


def compute_freq_loc(grid: list[list[str]]) -> dict[list[Point]]:
    result = defaultdict(list)
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c != ".":
                result[c].append(Point(x=i, y=j))
    return result

def in_bounds(grid: list[list[str]], point: Point) -> bool:
    m = len(grid)
    if m == 0:
        return False
    n = len(grid[0])
    return 0 <= point.x < m and 0 <= point.y < n

def compute_antinodes(grid: list[list[str]], a: Point, b: Point, allow_resonance: bool = False) -> list[Point]:
    """
    Computes the valid antinodes for a pair of points. They must be in bounds.
    If allow_resonance is False, can return either 0, 1 or 2 points.
    If allow_resonance is True, it will return as many as can fit on the map and the original two points.
    """
    result = []
    if allow_resonance:
        result.extend([a, b])
    vec1 = a - b
    anti1 = a + vec1
    while in_bounds(grid, anti1):
        result.append(anti1)
        if not allow_resonance:
            break
        anti1 += vec1
    vec2 = b - a 
    anti2 = b + vec2
    while in_bounds(grid, anti2):
        result.append(anti2)
        if not allow_resonance:
            break
        anti2 += vec2
    return result

def find_antinodes(grid: list[list[str]], allow_resonance: bool = False) -> int:
    freq_to_loc = compute_freq_loc(grid)
    node_locations = set()
    for freq, locations in freq_to_loc.items():
        for a, b in combinations(locations, 2):
            antinodes = compute_antinodes(grid, a, b, allow_resonance)
            # Process antinodes as needed
            for node in antinodes:
                node_locations.add(node)
    return len(node_locations)

if __name__ == "__main__":
    grid = parse_input("day_8/input.txt")
    num_antinodes = find_antinodes(grid)
    print(f"num_antinodes: {num_antinodes}")
    num_antinodes_with_resonance = find_antinodes(grid, allow_resonance=True)
    print(f"num_antinodes_with_resonance: {num_antinodes_with_resonance}")