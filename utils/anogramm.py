def is_anogram(string1: str, string2: str) -> bool:
    return sorted(string1.lower()) == sorted(string2.lower())

def collect_anograms(string: str, word_list: list):
    return [word for word in word_list if is_anogram(string, word)]