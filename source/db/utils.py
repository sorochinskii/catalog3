from re import findall


def split_and_concatenate(string: str) -> str:
    words = findall('.[^A-Z]*', string)
    result = "_".join(words)
    return result.lower()
