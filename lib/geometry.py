from dataclasses import dataclass
from typing import Any

@dataclass
class Vector:
    dx: int
    dy: int

    def __eq__(self, other: 'Vector') -> bool:
        return self.dx == other.dx and self.dy == other.dy

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
    
    def __str__(self) -> str:
        return f"({self.x},{self.y})"
    
    
CARDINAL_DIRECTIONS = [
    Vector(-1, 0),
    Vector(0, 1),
    Vector(1, 0),
    Vector(0, -1),
]

def get_next_cardinal_point(point: Point):
    for dir in CARDINAL_DIRECTIONS:
        next_point = point + dir
        yield next_point

def in_bounds(grid: list[list[Any]], point: Point) -> bool:
    m = len(grid)
    if m == 0:
        return False
    n = len(grid[0])
    return 0 <= point.x < m and 0 <= point.y < n
