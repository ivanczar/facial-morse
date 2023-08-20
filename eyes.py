from scipy.spatial import distance as dist


class Eyes:
    def __init__(self, config):
        self.EYE_AR_THRESH = float(config.get("EYE_AR_THRESH"))
        self.AR_CONSEC_FRAMES = int(config.get("AR_CONSEC_FRAMES"))
        self.ear = 0
        self.counter = 0
        self.total = 0

    def eye_aspect_ratio(self, left_eye, right_eye):
        A = dist.euclidean(left_eye[1], left_eye[5])
        B = dist.euclidean(left_eye[2], left_eye[4])
        C = dist.euclidean(left_eye[0], left_eye[3])
        D = dist.euclidean(right_eye[1], right_eye[5])
        E = dist.euclidean(right_eye[2], right_eye[4])
        F = dist.euclidean(right_eye[0], right_eye[3])

        left_ear = (A + B) / (2.0 * C)
        right_ear = (D + E) / (2.0 * F)
        self.ear = (left_ear + right_ear) / 2

    def detect_blink(self, morse_arr):
        if self.ear < self.EYE_AR_THRESH:
            self.counter += 1
        else:
            if self.counter >= 8:
                self.total += 1
                morse_arr.append("-")
            if 4 < self.counter < 8:
                self.total += 1
                morse_arr.append(".")
            self.counter = 0
