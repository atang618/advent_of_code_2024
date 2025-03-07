from collections import Counter

def read_input(filepath: str) -> tuple[list[int], list[int]]:
    with open(filepath, 'r') as file:
        first_list = []
        second_list = []
        for line in file:
            parts = line.split()
            first_list.append(int(parts[0]))
            second_list.append(int(parts[1]))
        return first_list, second_list

def compute_distances(first_list: list[int], second_list: list[int]) -> int:
    first_list.sort()
    second_list.sort()
    return sum([abs(x - y) for x, y in zip(first_list, second_list)])

def compute_similarity_score(first_list: list[int], second_list: list[int]) -> int:
    first_counter = Counter(first_list)
    second_counter = Counter(second_list)
    return sum((second_counter.get(key, 0) * key * value) for key, value in first_counter.items())


if __name__ == "__main__":
    list1, list2 = read_input("day_1/input.txt")
    distances = compute_distances(list1, list2)
    print(f"Sum: {distances}")
    score = compute_similarity_score(list1, list2)
    print(f"Similarity score: {score}")