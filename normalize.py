import re


def normalize(file_name: str) -> str:
    cyrillic_symbols = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя"
    latin_symbols = (
        "a", "b", "v", "h", "d", "e", "ie", "zh", "z", "y", "i", "i", "k", "l", "m", "n", "o", "p", "r", "s", "t",
        "u",
        "f", "kh", "ts", "ch", "sh", "shch", "", "i", "iu", "ia"
    )

    trans = {}

    for c, l in zip(cyrillic_symbols, latin_symbols):
        trans[ord(c)] = l
        trans[ord(c.upper())] = l.upper()

    new_file_name = file_name.translate(trans)
    pattern = r'[^a-zA-Z0-9]'
    for symbol in re.findall(pattern, new_file_name):
        new_file_name = new_file_name.replace(symbol, '_')
    return new_file_name
