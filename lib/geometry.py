from dataclasses import dataclass

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
    
    def __str__(self) -> str:
        return f"({self.x},{self.y})"