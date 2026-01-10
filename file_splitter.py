from math import ceil
import sys
# CHUNK_SIZE_MB: int = 50 #chunk size in megabytes
MAX_WORD_SIZE: int = 50 #upper bound on the maximum length of a word
CHUNK_SIZE: int = 10**6 - MAX_WORD_SIZE #chunk size in bytes
def get_chunk(start: int, end: int, file: str) -> str:
    while not file[start].isspace():
        start += 1
    while not file[end].isspace():
        end += 1
    return file[start: end]
with open(sys.argv[1], "r", encoding="UTF8") as file:
    content = file.read()
    for i in range(chunk_count:=(ceil((content_length := len(content)) / CHUNK_SIZE) - 1)):
        with open(f"{sys.argv[2]}-{i}.txt", "w", encoding="UTF8") as ofile:
            ofile.write(get_chunk(i * CHUNK_SIZE, min(content_length - 1, (i + 1) * CHUNK_SIZE), content))
        print(f"Chunk {i} of {chunk_count}")

        
