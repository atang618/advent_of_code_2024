from dataclasses import dataclass
from enum import Enum
import operator
from functools import partial

def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))

class Operator(Enum):
    ADD = operator.add
    MUL = operator.mul
    CONCAT = partial(concat)

@dataclass
class Equation:
    total: int
    values: list[int]

def parse_input(filepath: str) -> list[Equation]:
    result = []
    with open(filepath, "r") as file:
        for line in file:
            parts = line.split(':')
            assert len(parts) > 1
            result.append(Equation(total=int(parts[0]), values=list(map(int, parts[1].strip().split()))))
    return result

def check_equation(equation: Equation, allow_concat: bool = False) -> bool:
    def check_value(start_val: int, idx: int, op: Operator) -> bool:
        if idx > len(equation.values) - 1:
            return start_val == equation.total
        # Assuming add and multiply, we can early exit if already greater
        if start_val > equation.total:
            return False
        next_val = op.value(start_val, equation.values[idx])
        valid = check_value(next_val, idx+1, Operator.ADD) or check_value(next_val, idx+1, Operator.MUL)
        if allow_concat:
            valid |= check_value(next_val, idx+1, Operator.CONCAT)
        return valid

    return check_value(0, 0, Operator.ADD)
        
def check_equations(equations: list[Equation], allow_concat: bool = False) -> int:
    total = 0
    for equation in equations:
        if check_equation(equation, allow_concat):
            total += equation.total
    return total

if __name__ == "__main__":
    equations = parse_input("day_7/input.txt")
    sum_valid = check_equations(equations)
    print(f"sum_valid: {sum_valid}")
    sum_valid_with_concat = check_equations(equations, allow_concat=True)
    print(f"sum_valid_with_concat: {sum_valid_with_concat}")
