from dataclasses import dataclass

@dataclass
class Interval:
    start: int
    end: int

    def distance_to(self, val: int) -> int:
        if self.start <= val <= self.end:
            return 0
        return min(abs(self.start - val), abs(val - self.end))
    
    def __add__(self, other: 'Interval') -> 'Interval':
        return Interval(min(self.start, other.start), max(self.end, other.end))
    
    def __str__(self) -> str:
        return f'[{self.start},{self.end}]'

def distance_between_intervals(a: Interval, b: Interval) -> int:
    if b.start < a.start:
        return distance_between_intervals(b, a)
    
    if a.end < b.start:
        return a.distance_to(b.start)
    # They are overlapping
    return 0