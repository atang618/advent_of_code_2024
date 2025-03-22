import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.geometry import Point, Vector, CARDINAL_DIRECTIONS, in_bounds
from lib.math import Interval, distance_between_intervals
from dataclasses import dataclass, field
from copy import deepcopy

def parse_input(filepath: str) -> list[list[str]]:
    result = []
    with open(filepath, 'r') as file:
        for line in file:
            result.append(list(line.rstrip('\n')))
    return result

class Side:
    def __init__(self, direction: Vector, point: Point):
        self.direction = direction
        self.fixed_val = point.x if abs(self.direction.dx) > 0 else point.y
        # Inclusive interval
        non_fixed = point.y if abs(self.direction.dx) > 0 else point.x
        self.interval = Interval(non_fixed, non_fixed)

    @classmethod
    def from_values(cls, direction: Vector, fixed_val: int, interval: Interval) -> 'Side':
        instance = cls.__new__(cls)
        instance.direction = direction
        instance.fixed_val = fixed_val
        instance.interval = interval
        return instance

    def is_adjacent(self, other: 'Side') -> bool:
        if self.direction != other.direction:
            return False
        return self.fixed_val == other.fixed_val and distance_between_intervals(self.interval, other.interval) == 1
    
    def __add__(self, other: 'Side') -> 'Side':
        return Side.from_values(self.direction, self.fixed_val, self.interval + other.interval)

    def __str__(self) -> str:
        return f'{self.direction}, fixed: {self.fixed_val}, interval: {self.interval}'
    

@dataclass
class FenceInfo:
    area: int = 1
    perimeter: int = 0
    sides: list[Side] = field(default_factory=list)

    def __add__(self, other: 'FenceInfo') -> 'FenceInfo':
        area = self.area + other.area
        perimeter = self.perimeter + other.perimeter
        merged_sides = self._merge_sides(self.sides + other.sides)

        return FenceInfo(area, perimeter, merged_sides)

    def __str__(self) -> str:
        return f'Area: {self.area}, Perimeter: {self.perimeter}, Sides: {len(self.sides)}'

    def reduce(self) -> None:
        self.sides = self._merge_sides(self.sides)

    @staticmethod
    def _merge_sides(sides: list[Side]) -> list[Side]:
        merged_sides = []
        visited = set()

        for i, side in enumerate(sides):
            if i in visited:
                continue
            merged = side
            for j, other_side in enumerate(sides):
                if j != i and j not in visited and merged.is_adjacent(other_side):
                    merged += other_side  # Use the `__add__` method to merge
                    visited.add(j)
            merged_sides.append(merged)
            visited.add(i)

        return merged_sides

    def cost(self) -> int:
        return self.area * self.perimeter
    
    def bulk_cost(self) -> int:
        return self.area * len(self.sides)

TRAVERSED_VAL = '.'

def get_fence_info(grid: list[list[str]], point: Point, visited: set) -> FenceInfo:
    fence_info = FenceInfo()
    current_val = grid[point.x][point.y]
    visited.add(point)
    for dir in CARDINAL_DIRECTIONS:
        next_point = point + dir
        if next_point in visited:
            continue
        if not in_bounds(grid, next_point) or grid[next_point.x][next_point.y] != current_val: 
            fence_info.perimeter += 1
            fence_info.sides.append(Side(dir, point))
            continue
        fence_info += get_fence_info(grid, next_point, visited)
    grid[point.x][point.y] = TRAVERSED_VAL
    fence_info.reduce()
    return fence_info

def compute_fence_cost(grid: list[list[str]], use_bulk: bool = False) -> int:
    m = len(grid)
    n = len(grid[0])
    cost = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] != TRAVERSED_VAL:
                point = Point(i, j)
                visited = set()
                fence_info = get_fence_info(grid, point, visited)
                cost += fence_info.bulk_cost() if use_bulk else fence_info.cost()
    return cost

if __name__ == "__main__":
    grid = parse_input("day_12/input.txt")
    cost = compute_fence_cost(deepcopy(grid))
    print(f'Fence cost: {cost}')
    bulk_cost = compute_fence_cost(deepcopy(grid), use_bulk=True)
    print(f"Bulk fence cost: {bulk_cost}")
