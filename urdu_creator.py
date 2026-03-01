words: list[tuple[str, str]]
urdu: list[str] = []
english: list[str] = []
is_urdu: bool = True

def check_is_english(string: str):
    count = 0
    for char in string:
        if char.isalpha() or char in ".()/":
            count += 1
    if count/len(string) > 0.5:
        return True
    else:
        print(string, count, len(string), count/len(string))
        return False

with open("urdu.txt", "r", encoding="UTF8") as file:
    for line in file:
        if is_urdu:
            urdu.append(line.strip())
        else:
            english.append(line.strip())
            assert check_is_english(line.strip())
        is_urdu = not is_urdu
assert len(urdu) == len(english), "lengths were not equal"
with open("out_urdu.psv", "w", encoding="UTF8") as file:
    file.write("\n".join(f"{urdu_word} | {english_word}" for urdu_word, english_word in zip(urdu, english)))