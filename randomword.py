import random

easy = ["host", "give", "land", "pace", "mist", "stem", "bite", "coma", "help"]
difficult = [
    "cottages",
    "riddance",
    "sluggish",
    "speeders",
    "sootiest",
    "yielding",
    "nerdiest",
    "seabirds",
    "jabbered",
]


class RandomWord:
    difficulty = ""
    word = ""
    color_bool_array = []

    def __init__(self, is_easy=True):
        self.is_easy = is_easy
        self.word = self.generate_random_word()
        self.color_bool_array = self.generate_color_bool_arr(self.word)

    def generate_random_word(self):
        if self.is_easy:
            return random.choice(easy).upper()
        else:
            return random.choice(difficult).upper()

    def generate_color_bool_arr(self, word):
        array = []
        for i in range(0, len(word)):
            array.append(None)
        return array

    def update_color_arr(self, index, value):
        self.color_bool_array[index] = value

    def get_green_count(self):
        return self.color_bool_array.count(True)

    def get_red_count(self):
        return self.color_bool_array.count(False)
