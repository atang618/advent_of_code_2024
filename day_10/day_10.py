import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.geometry import Point, Vector, CARDINAL_DIRECTIONS

def parse_input(filepath: str) -> list[list[int]]:
    result = []
    with open(filepath, 'r') as file:
        for line in file:
            result.append([int(char) for char in line.strip()])
    return result

class Solver:
    def __init__(self, grid: list[list[int]]):
        self.grid = grid
        self.m = len(grid)
        self.n = len(grid[0])
        self.memo_scores = dict()
        self.memo_rating = dict()
        self.directions = CARDINAL_DIRECTIONS

    def compute_scores(self) -> int:
        total_score = 0
        for i in range(self.m):
            for j in range(self.n):
                point = Point(i, j)
                if self._get(point) == 0:
                    score = len(self._get_score(point))
                    # print(f"Point {point} score: {score}")
                    total_score += score
        return total_score

    def compute_ratings(self) -> int:
        total_rating = 0
        for i in range(self.m):
            for j in range(self.n):
                point = Point(i, j)
                if self._get(point) == 0:
                    rating = self._get_rating(point)
                    total_rating += rating
        return total_rating

    def _set(self, point: Point, val: int) -> None:
        self.grid[point.x][point.y] = val

    def _get(self, point: Point) -> int:
        return self.grid[point.x][point.y]

    def _in_bounds(self, point: Point) -> bool:
        return 0 <= point.x < self.m and 0 <= point.y < self.n

    def _get_next_spot(self, point: Point, val: int):
        for dir in self.directions:
            next_point = point + dir
            if not self._in_bounds(next_point):
                continue
            if self._get(next_point) == -1:
                continue
            if (self._get(next_point) - val) != 1:
                continue
            yield next_point

    def _get_score(self, point: Point) -> set:
        if point in self.memo_scores:
            return self.memo_scores[point].copy()
        result = set()
        if self._get(point) == 9:
            result.add(point)
            return result
        val = self._get(point)
        self._set(point, -1)
        for next_point in self._get_next_spot(point, val):
            result.update(self._get_score(next_point))
        self._set(point, val)
        self.memo_scores[point] = result.copy()
        return result
    
    def _get_rating(self, point: Point) -> int:
        if point in self.memo_rating:
            return self.memo_rating[point]
        if self._get(point) == 9:
            return 1
        rating = 0
        val = self._get(point)
        self._set(point, -1)
        for next_point in self._get_next_spot(point, val):
            rating += self._get_rating(next_point)
        self._set(point, val)
        self.memo_rating[point] = rating
        return rating

if __name__ == "__main__":
    grid = parse_input("day_10/input.txt")
    solver = Solver(grid)
    score = solver.compute_scores()
    print(f"Score: {score}")
    rating = solver.compute_ratings()
    print(f"Rating: {rating}")