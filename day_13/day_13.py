import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.geometry import Point, Vector
from dataclasses import dataclass, field

TOKEN_COST = {
    'a': 3,
    'b': 1,
}

@dataclass
class ClawMachine:
    a: Vector = field(default_factory=Vector)
    b: Vector = field(default_factory=Vector)
    prize: Point = field(default_factory=Point)

def parse_input(filepath: str) -> list[ClawMachine]:
    machines = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 4):
            a_line = lines[i].strip()
            b_line = lines[i + 1].strip()
            prize_line = lines[i + 2].strip()
            # Get after the colon
            a_coords = a_line.split(':')[1].strip().split(', ')
            b_coords = b_line.split(':')[1].strip().split(', ')
            prize_coords = prize_line.split(':')[1].strip().split(', ')
            # assumes X+,Y+ for buttons, and X=,Y= for prize
            a = Vector(int(a_coords[0][2:]), int(a_coords[1][2:]))
            b = Vector(int(b_coords[0][2:]), int(b_coords[1][2:]))
            prize = Point(int(prize_coords[0][2:]), int(prize_coords[1][2:]))

            machines.append(ClawMachine(a, b, prize))
        return machines
    
def compute_min_cost(loc: Point, machine: ClawMachine, tokens_used: int, memo: dict) -> int:
    if loc == machine.prize:
        return tokens_used
    if (loc, tokens_used) in memo:
        return memo[(loc, tokens_used)]
    def is_valid(point: Point) -> bool:
        return point.x <= machine.prize.x and point.y <= machine.prize.y
    next_point = loc + machine.a
    min_cost = float('inf')
    if is_valid(next_point):
        min_cost = min(min_cost, compute_min_cost(next_point, machine, tokens_used+TOKEN_COST['a'], memo))
    next_point = loc + machine.b
    if is_valid(next_point):
        min_cost = min(min_cost, compute_min_cost(next_point, machine, tokens_used+TOKEN_COST['b'], memo))
    memo[((loc, tokens_used))] = min_cost
    return min_cost

def compute_all_prizes(machines: list[ClawMachine]) -> int:
    total_cost = 0
    for machine in machines:
        cost = compute_min_cost(Point(0,0), machine, 0, dict())
        if cost != float('inf'):
            total_cost += cost

    return total_cost

if __name__ == '__main__':
    machines = parse_input('day_13/input.txt')
    cost = compute_all_prizes(machines)
    print(f'Cost to win: {cost}')
