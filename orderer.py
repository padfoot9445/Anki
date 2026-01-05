from sys import argv
from typing import Literal


def load_frequency(path: str) -> dict[str, int]:
    out:dict[str, int] = {}
    with open(path, "r", encoding="UTF8") as file:
        lines = file.readlines()
        for line in lines:
            x = line.split(" ")
            assert len(x) == 2
            word, count = x
            out[word] = int(count)
    return out

def load_cards(path:str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    with open(path, "r", encoding="UTF8") as file:
        lines = file.readlines()
        for line in lines:
            if line[0] == "#":
                continue
            x = line.strip().split("\t")
            if len(x) != 2:
                print(f"ERROR: {x} could not be parsed")
                continue
            k, v = x
            out.append((k, v))
    return out

DIVIDER: Literal["__DIVIDER__"] = "__DIVIDER__"

def find_frequency(word: str, freq:dict[str, int]) -> int:
    if word == DIVIDER: return -1
    words:list[str] = []
    s = j = 0
    while j < len(word):
        if not word[j].isalpha():
            words.append(word[s:j])
            s = j + 1
        j += 1
    if s != j:
        words.append(word[s:j])
    freqs = [freq[x.lower()] for x in words if x.lower() in freq]
    return min(freqs) if len(freqs) > 0 else -2

def out_cards(cards: list[tuple[str, str]]) -> str:
    return "\n".join(f"{v}\t{i}\t{j}" for v, (i, j) in enumerate(cards))

if __name__ == "__main__":
    
    if (argc := len(argv)) != 5 or (argc >= 2 and argv[1] == "--help"):
        print("Usage: python3 orderer.py [frequency list path] [unsorted notes (tsv) path] [output file path] [unknown words path]")
    freq = load_frequency(argv[1])
    cards = load_cards(argv[2]) + [(DIVIDER, DIVIDER)]
    out = argv[3]
    cards.sort(key=lambda x: (find_frequency(x[0], freq), -len(x[0])), reverse=True)
    divider_index = cards.index((DIVIDER, DIVIDER))
    unknown_cards = cards[divider_index + 1:] if divider_index + 1 < len(cards) else []
    known_cards = cards[:divider_index]
    with open(out, "w", encoding="UTF8") as file:
        file.write(out_cards(known_cards))
    with open(argv[4], "w", encoding="UTF8") as file:
        file.write(out_cards(unknown_cards))