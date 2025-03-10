from typing import Optional
import functools

def read_input(filepath: str) -> list[list]:
    result = []
    with open(filepath, 'r') as file:
        for line in file:
            result.append(list(map(int, line.split())))
    return result

def has_violation(dist: int, dir: bool, prev_dir: Optional[bool]) -> bool:
    return dist < 1 or dist > 3 or (prev_dir is not None and dir != prev_dir)

def is_safe_strict(report: list[int]) -> bool:
    n = len(report)
    if n < 2:
        return True
    prev_dir = None
    for i in range(n-1):
        delta = report[i+1] - report[i]
        dist = abs(delta)
        dir = delta > 0
        if has_violation(dist, dir, prev_dir):
            return False
        prev_dir = dir
    return True

# 5 4 5 6 7 -> remove 5
# 5 2 6 7 8 -> remove 2

def is_safe_dampener(report: list[int]) -> bool:
    if is_safe_strict(report):
        return True
    n = len(report)

    for i in range(0, n):
        if is_safe_strict(report[:i] + report[i+1:]):
            return True
    return False

class ReportChecker:
    def __init__(self, report: list[int]):
        self.report = report

    @functools.cache
    def is_safe_dampener(self, prev_idx: int, curr_idx: int, prev_dir: Optional[bool], tol: int) -> bool:
        if curr_idx > len(self.report)-1:
            return True
        violation = False
        dir = prev_dir
        if prev_idx > -1:
            delta = self.report[curr_idx] - self.report[prev_idx]
            dist = abs(delta)
            dir = delta > 0
            violation = has_violation(dist, dir, prev_dir)
        # Check keep
        is_safe = not violation and self.is_safe_dampener(curr_idx, curr_idx+1, dir, tol)
        if tol > 0:
            # Check not keep
            is_safe |= self.is_safe_dampener(prev_idx, curr_idx+1, prev_dir, tol-1)
        return is_safe

if __name__ == "__main__":
    reports = read_input("day_2/input.txt")
    num_safe = sum(is_safe_strict(report) for report in reports)
    print(f"num_safe_strict: {num_safe}")
    num_safe_dampener = sum(is_safe_dampener(report) for report in reports)
    print(f"num_safe_dampener: {num_safe_dampener}")