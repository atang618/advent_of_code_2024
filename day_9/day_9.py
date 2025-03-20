from dataclasses import dataclass, field
from copy import deepcopy

@dataclass
class Chunk:
    id: int
    idx: int
    size: int

@dataclass
class Memory:
    # Both chunks are ordered by index
    used_chunks: list[Chunk] = field(default_factory=list)
    free_chunks: list[Chunk] = field(default_factory=list)

    def file_blocks(self) -> list[int]:
        result = []
        used_ptr, free_ptr = 0, 0

        while used_ptr < len(self.used_chunks) or free_ptr < len(self.free_chunks):
            # print(f"{used_ptr}, {free_ptr}")
            used = self.used_chunks[used_ptr] if used_ptr < len(self.used_chunks) else None
            free = self.free_chunks[free_ptr] if free_ptr < len(self.free_chunks) else None

            if free is None or (used is not None and used.idx < free.idx):
                result.extend([used.id] * used.size)
                used_ptr += 1
            else:
                result.extend([free.id] * free.size)
                free_ptr += 1

        return result

def parse_input(filepath: str) -> Memory:
    mem = Memory()
    with open(filepath, 'r') as file:
        line = file.readline().rstrip('\n')
        id = 0
        idx = 0
        for i, c in enumerate(line):
            size = int(c)
            chunk = Chunk(id=id, idx=idx, size=size)
            if i % 2 == 0:
                mem.used_chunks.append(chunk)
                id += 1
            else:
                chunk.id = -1
                mem.free_chunks.append(chunk)
            idx += size
    return mem

def rearrange_file_blocks(file_blocks: list[int]) -> list[int]:
    n = len(file_blocks)
    l = 0
    r = n - 1
    def move_to_next_file(r: int) -> int:
        while r > -1 and file_blocks[r] == -1:
            r -= 1
        return r
    r = move_to_next_file(r)
    while l < r:
        if file_blocks[l] == -1:
            file_blocks[l] = file_blocks[r]
            file_blocks[r] = -1
            r = move_to_next_file(r)
        l += 1
    return file_blocks

def rearrange_file_chunks(mem: Memory) -> Memory:
    updated_used_chunks = []
    added_free_chunks = []
    while mem.used_chunks:
        used_chunk = mem.used_chunks.pop()
        relocated = False
        for i, free_chunk in enumerate(mem.free_chunks):
            if free_chunk.idx > used_chunk.idx:
                break

            if used_chunk.size <= free_chunk.size:
                added_free_chunks.append(Chunk(id=-1, idx=used_chunk.idx, size=used_chunk.size))
                used_chunk.idx = free_chunk.idx                
                free_chunk.idx += used_chunk.size
                free_chunk.size -= used_chunk.size
                updated_used_chunks.append(used_chunk)
                relocated = True
                if free_chunk.size <= 0:
                    mem.free_chunks.pop(i)
                break
        if not relocated:
            updated_used_chunks.append(used_chunk)

    mem.used_chunks = updated_used_chunks
    mem.used_chunks.sort(key=lambda chunk: chunk.idx)
    mem.free_chunks.extend(added_free_chunks)
    mem.free_chunks.sort(key=lambda chunk: chunk.idx)

    return mem

def compute_checksum(file_blocks: list[int]) -> int:
    return sum(i * val if val > -1 else 0 for i, val in enumerate(file_blocks))

if __name__ == "__main__":
    memory = parse_input("day_9/input.txt")
    file_blocks = rearrange_file_blocks(deepcopy(memory.file_blocks()))
    checksum = compute_checksum(file_blocks)
    print(f"check_sum: {checksum}")
    rearranged_memory = rearrange_file_chunks(memory)
    chunked_file_blocks = rearranged_memory.file_blocks()
    chunked_check_sum = compute_checksum(chunked_file_blocks)
    print(f"chunked_check_sum: {chunked_check_sum}")
