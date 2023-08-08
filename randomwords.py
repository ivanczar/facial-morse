import random

easy = ["host", "give", "land", "pace", "mist", "stem", "bite", "coma", "help"]
# hard = ["host", "give", "land", "pace", "mist", "stem", "bite", "coma", "help"]


#  Make a dictionary where key is word string, value is array of booleans (null = grey, true = green, false = red)


def get_word_dict():
    word = random.choice(easy).upper()
    dictionary = {}
    array = []
    for i in range(0, len(word)):
        array.append(None)
    dictionary[word] = array
    return dictionary


# w = get_word_dict(easy)
# print(w)
# word = list(w.keys())[0]
# print(w[word])
