from dataclasses import dataclass
import math 
from collections import defaultdict

@dataclass
class Input:
    prereqs: dict[int, list[int]]
    updates: list[list[int]]

def parse_file(filepath: str) -> Input:
    prereqs = defaultdict(list)
    updates = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines) and lines[i].strip():
            parts = list(map(int, lines[i].split('|')))
            assert len(parts) == 2
            prereqs[parts[0]].append(parts[1])
            i += 1
        i += 1  # Skip the empty line
        while i < len(lines):
            updates.append(list(map(int, lines[i].split(','))))
            i += 1
    return Input(prereqs=prereqs, updates=updates)

def is_valid_update(update: list[int], prereqs: dict[int, list[int]]) -> bool:
    seen = set()
    for page in update:
        if any(x in seen for x in prereqs[page]):
            # print(f"Invalid update: {update}, {page}, {input.prereqs[page]}")
            return False
        seen.add(page)
    return True

def compute_mid_number(input: Input) -> int:
    total = 0
    for update in input.updates:
        if is_valid_update(update, input.prereqs):
            mid = update[len(update)//2]
            total += mid
    return total

def fix_invalid_updates(input: Input) -> int:
    total = 0
    for update in input.updates:
        i = 0
        n = len(update)
        fixed = False
        while i < n:
            page = update[i]
            for j in range(i):
                # Find the earliest value page has to be ahead of
                if update[j] in input.prereqs[page]:
                    update.pop(i)
                    update.insert(j, page)
                    fixed = True
                    break
            i += 1
        if fixed:
            mid = update[len(update)//2]
            total += mid
    return total

if __name__ == "__main__":
    input = parse_file("day_5/input.txt")
    mid_sum = compute_mid_number(input)
    print(f"mid_sum: {mid_sum}")
    fixed_mid_sum = fix_invalid_updates(input)
    print(f"fixed_mid_sum: {fixed_mid_sum}")
