import configparser

from scipy.spatial import distance as dist

from morse_to_english import morse_to_english


class Blinks:
    def __init__(self):
        config_data = configparser.ConfigParser()
        config_data.read("config.ini")
        blink_config = config_data["BLINK"]
        cv2_config = config_data["CV2"]
        self.EYE_AR_THRESH = float(blink_config.get("EYE_AR_THRESH"))
        self.MOUTH_AR_THRESH = float(blink_config.get("MOUTH_AR_THRESH"))
        self.AR_CONSEC_FRAMES = int(blink_config.get("AR_CONSEC_FRAMES"))
        self.left_ear = 0
        self.right_ear = 0
        self.mar = 0
        self.left_eye_counter = 0
        self.right_eye_counter = 0
        self.mouth_counter = 0
        self.left_eye_total = 0
        self.right_eye_total = 0
        self.mouth_total = 0

    def eye_aspect_ratio(self, left_eye, right_eye):
        A = dist.euclidean(left_eye[1], left_eye[5])
        B = dist.euclidean(left_eye[2], left_eye[4])
        C = dist.euclidean(left_eye[0], left_eye[3])
        D = dist.euclidean(right_eye[1], right_eye[5])
        E = dist.euclidean(right_eye[2], right_eye[4])
        F = dist.euclidean(right_eye[0], right_eye[3])

        self.left_ear = (A + B) / (2.0 * C)
        self.right_ear = (D + E) / (2.0 * F)

    def mouth_aspect_ratio(self, mouth):
        A = dist.euclidean(mouth[2], mouth[10])
        B = dist.euclidean(mouth[4], mouth[8])
        C = dist.euclidean(mouth[0], mouth[6])
        self.mar = (A + B) / (2.0 * C)

    def detect_blink(self, morse_arr):
        if self.left_ear < self.EYE_AR_THRESH:
            self.left_eye_counter += 1
        if self.right_ear < self.EYE_AR_THRESH:
            self.right_eye_counter += 1
        else:
            if self.left_eye_counter >= self.AR_CONSEC_FRAMES:
                self.left_eye_total += 1
                morse_arr.append(".")
            if self.right_eye_counter >= self.AR_CONSEC_FRAMES:
                self.right_eye_total += 1
                morse_arr.append("-")
            self.left_eye_counter = 0
            self.right_eye_counter = 0

    def detect_mouth(
        self,
        english_arr,
        morse_arr,
        random_word,
    ):
        if self.mar > self.MOUTH_AR_THRESH:
            self.mouth_counter += 1
        else:
            if self.mouth_counter >= self.AR_CONSEC_FRAMES:
                if (
                    self.left_eye_total == 0
                    and self.right_eye_total == 0
                    and english_arr
                ):
                    pop_index = len(english_arr) - 1
                    random_word.update_color_arr(pop_index, None)
                    english_arr.pop()
                    mouth_total = 0
                else:
                    self.mouth_total += 1
                    left_total = 0
                    right_total = 0
                    morse_to_english(morse_arr, english_arr)
                    morse_arr.clear()
            self.mouth_counter = 0
