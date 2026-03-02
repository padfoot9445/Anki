def line_to_word_pair(line: str) -> tuple[str, str]:
    if line[-1] == "*":
        line = line[:-1]
    
    start = current = 0
    
    while True:
        x = find_bracket(line, current)
        if x == None:
            break
        else:
            start, current = x

    return line[:start].strip(), line[start + 1: -1].strip()

def find_bracket(line: str, start: int) -> tuple[int, int] | None:
    start = line.find('(', start)

    if start == -1:
        return None

    try:
        stack = 0
        current = start

        assert line[current] == '(', f"expected '('; got {line[current]} at {current} in {line}"

        while True:
            if line[current] == '(':
                stack += 1
            elif line[current] == ')':
                stack -= 1
            if stack == 0:
                break
            current += 1
        
        return start, current
    except IndexError:
        print(f"Unpaired opening bracket in section beginning {start} in {line}")
        return start, len(line) - 1








with open("spanish.txt", "r", encoding="UTF8") as file:
    words = [line_to_word_pair(line.strip()) for line in file]

with open("out_spanish.txt", "w", encoding="UTF8") as file:
    file.write("\n".join(f"{spanish}\t{english}" for spanish, english in words))
