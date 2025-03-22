import functools
from typing import Optional
from tqdm import tqdm

def parse_input(filepath: str) -> list[int]:
    with open(filepath, 'r') as file:
        line = file.readline()
        return list(map(int, line.rstrip('\n').split()))

class Node:
    def __init__(self, val: int, prev: Optional['Node'] = None, next: Optional['Node'] = None):
        self.val = val
        self.prev = prev
        self.next = next

class Simulation:
    def __init__(self, stones: list[int]):
        self.head = Node(-1)
        node = self.head
        for stone in stones:
            node.next = Node(stone, prev=node)
            node = node.next
        self.max_steps = 0
    
    def run_iterative(self, num_steps: int) -> int:
        result = 0
        for _ in tqdm(range(num_steps), desc="Running simulation"):
            result = self._step()
        return result

    def run_dfs(self, num_steps: int) -> int:
        self.max_steps = num_steps
        node = self.head.next
        num_stones = 0
        while node:
            num_stones += self._dfs(node.val, 0)
            node = node.next
        return num_stones

    @staticmethod
    def get_num_digits(val: int) -> int:
        n = 0
        temp_val = val
        while temp_val > 0:
            temp_val //= 10
            n += 1
        return n

    @functools.cache
    def _dfs(self, val: int, step: int) -> int:
        if step == self.max_steps:
            return 1
        if val == 0:
            return self._dfs(1, step + 1)
        n = self.get_num_digits(val)
        if n % 2 == 0:
            divisor = 10 ** (n // 2)
            return self._dfs(val // divisor, step + 1) + self._dfs(val % divisor, step + 1)
        return self._dfs(val * 2024, step + 1)

    def _step(self) -> int:
        num_stones = 0
        node = self.head.next
        while node:
            if node.val == 0:
                node.val = 1
                num_stones += 1
                node = node.next
                continue
            n = self.get_num_digits(node.val)
            if n % 2 == 0:
                divisor = 10 ** (n // 2)
                second = Node(node.val % divisor, prev=node, next=node.next)
                node.val //= divisor
                node.next = second
                num_stones += 2
                node = second.next
                continue
            node.val *= 2024
            num_stones += 1
            node = node.next
        return num_stones


if __name__ == "__main__":
    stones = parse_input("day_11/input.txt")
    sim = Simulation(stones)
    num_stones = sim.run_dfs(25)
    print(f'num_stones after 25 steps: {num_stones}')
    sim = Simulation(stones)
    num_stones = sim.run_dfs(75)
    print(f'num_stones after 75 steps: {num_stones}')