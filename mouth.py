from scipy.spatial import distance as dist

from morse_to_english import morse_to_english


# TODO: Separate into Eye and Mouth Class and inherit from abstract Landmark class
class Mouth:
    def __init__(self, config, eyes):
        self.MOUTH_AR_THRESH = float(config.get("MOUTH_AR_THRESH"))
        self.AR_CONSEC_FRAMES = int(config.get("AR_CONSEC_FRAMES"))
        self.mar = 0
        self.counter = 0
        self.total = 0
        self.eyes = eyes

    def mouth_aspect_ratio(self, mouth):
        A = dist.euclidean(mouth[2], mouth[10])
        B = dist.euclidean(mouth[4], mouth[8])
        C = dist.euclidean(mouth[0], mouth[6])
        self.mar = (A + B) / (2.0 * C)

    def detect_mouth(
        self,
        english_arr,
        morse_arr,
        random_word,
    ):
        if self.mar > self.MOUTH_AR_THRESH:
            self.counter += 1
        else:
            if self.counter >= self.AR_CONSEC_FRAMES:
                if (
                    self.eyes.left_total == 0
                    and self.eyes.right_total == 0
                    and english_arr
                ):
                    pop_index = len(english_arr) - 1
                    random_word.update_color_arr(pop_index, None)
                    english_arr.pop()
                    self.total = 0
                else:
                    self.total += 1
                    self.eyes.left_total = 0
                    self.eyes.right_total = 0
                    morse_to_english(morse_arr, english_arr)
                    morse_arr.clear()
            self.counter = 0
