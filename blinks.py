import configparser

from scipy.spatial import distance as dist

from morse_to_english import morse_to_english


class Blinks:
    EYE_AR_THRESH = 0
    MOUTH_AR_THRESH = 0
    AR_CONSEC_FRAMES = 0

    def __init__(self):
        config_data = configparser.ConfigParser()
        config_data.read("config.ini")
        blink_config = config_data["BLINK"]
        cv2_config = config_data["CV2"]
        self.EYE_AR_THRESH = float(blink_config.get("EYE_AR_THRESH"))
        self.MOUTH_AR_THRESH = float(blink_config.get("MOUTH_AR_THRESH"))
        self.AR_CONSEC_FRAMES = int(blink_config.get("AR_CONSEC_FRAMES"))

    def eye_aspect_ratio(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def mouth_aspect_ratio(self, mouth):
        A = dist.euclidean(mouth[2], mouth[10])
        B = dist.euclidean(mouth[4], mouth[8])
        C = dist.euclidean(mouth[0], mouth[6])
        mar = (A + B) / (2.0 * C)
        return mar

    def detect_blink(
        self, eye_aspect_ratio, eye_counter, eye_total, blink_char, morse_arr
    ):
        if eye_aspect_ratio < self.EYE_AR_THRESH:
            eye_counter += 1
        else:
            if eye_counter >= self.AR_CONSEC_FRAMES:
                eye_total += 1
                morse_arr.append(blink_char)
            eye_counter = 0
        return eye_counter, eye_total

    def detect_mouth(
        self,
        english_arr,
        morse_arr,
        mouth_aspect_ratio,
        random_word,
        mouth_total,
        mouth_counter,
        left_eye_total,
        right_eye_total,
    ):
        if mouth_aspect_ratio > self.MOUTH_AR_THRESH:
            mouth_counter += 1
        else:
            if mouth_counter >= self.AR_CONSEC_FRAMES:
                if left_eye_total == 0 and right_eye_total == 0 and english_arr:
                    pop_index = len(english_arr) - 1
                    random_word.update_color_arr(pop_index, None)
                    english_arr.pop()
                    mouth_total = 0
                else:
                    mouth_total += 1
                    left_total = 0
                    right_total = 0
                    morse_to_english(morse_arr, english_arr)
                    morse_arr.clear()
            mouth_counter = 0
        return mouth_counter, mouth_total, left_eye_total, right_eye_total
