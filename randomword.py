import random

easy = ["host", "give", "land", "pace", "mist", "stem", "bite", "coma", "help"]


class RandomWord:
    difficulty = ""
    word = ""
    color_bool_array = []

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.word = self.generate_random_word()
        self.color_bool_array = self.generate_color_bool_arr(self.word)

    def generate_random_word(self):
        random_word = random.choice(easy).upper()
        return random_word

    def generate_color_bool_arr(self, word):
        array = []
        for i in range(0, len(word)):
            array.append(None)
        return array

    def update_color_arr(self, index, value):
        self.color_bool_array[index] = value


# test = RandomWord("easy")
# print(test.word)
# print(test.color_bool_array)
