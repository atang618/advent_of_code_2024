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

def parse_input(filepath: str, offset: int = 0) -> list[ClawMachine]:
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
            prize = Point(int(prize_coords[0][2:]) + offset, int(prize_coords[1][2:]) + offset)

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

def linear_solve(machine: ClawMachine) -> int:
    """
    2 equations, 2 unknowns:
    a * x_a + b * x_b = x_p
    a * y_a + b * y_b = y_p

    a = (x_p - b * x_b) / x_a
    b = (y_p * x_a - x_p * y_a) / (y_p * x_a - x_b * y_a)
    """
    x_a, y_a = machine.a.dx, machine.a.dy
    x_b, y_b = machine.b.dx, machine.b.dy
    x_p, y_p = machine.prize.x, machine.prize.y
    b = (y_p * x_a - x_p * y_a) / (y_b * x_a - x_b * y_a)
    if not b.is_integer():
        return float('inf')
    b = int(b)
    a = (x_p - b * x_b) / x_a
    if not a.is_integer():
        return float('inf')
    a = int(a)
    return a * TOKEN_COST['a'] + b * TOKEN_COST['b']


def compute_all_prizes(machines: list[ClawMachine]) -> int:
    total_cost = 0
    for machine in machines:
        cost = linear_solve(machine)
        if cost != float('inf'):
            total_cost += cost

    return total_cost

if __name__ == '__main__':
    filepath = 'day_13/input.txt'
    machines = parse_input(filepath)
    cost = compute_all_prizes(machines)
    print(f'Cost to win: {cost}')
    offset = 10000000000000
    machines = parse_input(filepath, offset)
    cost = compute_all_prizes(machines)
    print(f'Cost to win with offset {cost}')
