from typing import Optional

def parse_input_txt(filepath: str) -> str:
    with open(filepath, 'r') as file:
        return file.read()

def get_close_paren_idx(text: str, start: int) -> Optional[int]:
    while start < len(text) and text[start] != ')':
        start += 1
    if start == len(text):
        return None
    return start 

def get_valid_int(input: str) -> Optional[int]:
    if len(input) > 3:
        return None
    val = 0
    for c in input:
        if not c.isdigit():
            return None
        val = 10 * val + int(c)
    return val

def parse_mul(input: str) -> Optional[int]:
    parts = input.split(',')
    if len(parts) != 2:
        return None
    a, b = get_valid_int(parts[0]), get_valid_int(parts[1])
    if a is None or b is None:
        return None
    return a * b

def get_valid_mul(text: str) -> int:
    i = 0
    sum = 0
    while i < len(text):
        if text[i:i+4] == "mul(":
            j = get_close_paren_idx(text, i+3)
            if j is not None:
                out = parse_mul(text[i+4:j])
                if out is not None:
                    sum += out
                    i = j
        i += 1
    return sum

def get_valid_mul_enabled(text: str) -> int:
    i = 0
    sum = 0
    enabled = True
    while i < len(text):
        if enabled and text[i:i+4] == "mul(":
            j = get_close_paren_idx(text, i+3)
            if j is not None:
                out = parse_mul(text[i+4:j])
                if out is not None:
                    sum += out
                    i = j
        if text[i:i+4] == "do()":
            enabled = True
        if text[i:i+7] == "don't()":
            enabled = False
        i += 1
    return sum

if __name__ == "__main__":
    text = parse_input_txt("day_3/input.txt")
    valid_mul_total = get_valid_mul(text)
    print(f"valid_mul_total: {valid_mul_total}")
    enabled_mul_total = get_valid_mul_enabled(text)
    print(f"enabled_mul_total: {enabled_mul_total}")

