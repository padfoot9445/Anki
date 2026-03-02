def line_to_word_pair(line: str) -> tuple[str, str]:
    if line[-1] == "*":
        line = line[:-1]
    current = 0
    try:
        while line[current] != '(':
            current += 1
    except IndexError:
        print(line)
        raise

    return line[:current].strip(), line[current + 1: -1].strip()



with open("spanish.txt", "r", encoding="UTF8") as file:
    words = [line_to_word_pair(line.strip()) for line in file]

with open("out_spanish.txt", "w", encoding="UTF8") as file:
    file.write("\n".join(f"{spanish}|{english}" for spanish, english in words))
