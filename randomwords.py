import random

words = ["host", "give", "land", "pace", "mist", "stem", "bite", "coma", "help"]


def getWordDict():
    word = random.choice(words).upper()
    dict = {}
    for letter in word:
        dict[letter] = (129, 129, 129)
    return dict
