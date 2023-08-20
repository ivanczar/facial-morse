class Logger:
    def __init__(self, word):
        self.file_path = "./game_logs.txt"
        self.num_lines = self.count_lines()
        self.word = word
        self.create_entry()

    def count_lines(self):
        with open(self.file_path) as f:
            return sum(1 for _ in f)

    def create_entry(self):
        f = open(self.file_path, "a")
        f.write(f"{self.num_lines + 1}. {self.word}: Errors:0  Correct:0 \n")
        f.close()

    def update_errors(self):
        f = open(self.file_path, "r+")
        content = f.readlines()
        line = content[self.num_lines]
        error_token = line.split(" ")[2]
        updated_error_count = int(error_token.split(":")[1]) + 1
        f.write(
            f"{self.num_lines}. {self.word}: Errors:{updated_error_count}  Correct: \n"
        )
        f.close()

    # def update_corrects(self):
    #     f = open(self.file_path, "w")
    #     content = f.readlines()
    #     line = content[self.num_lines]
    #     correct_token = line.split(" ")[3]
    #     updated_correct_count = int(correct_token.split(":")[1]) + 1
    #     f.write(f"{self.num_lines}. {self.word}: Errors:{updated_error_count}  Correct: \n")
