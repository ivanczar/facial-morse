from scipy.spatial import distance as dist


class Eyes:
    def __init__(self, config):
        self.EYE_AR_THRESH = float(config.get("EYE_AR_THRESH"))
        self.AR_CONSEC_FRAMES = int(config.get("AR_CONSEC_FRAMES"))
        self.left_ear = 0
        self.right_ear = 0
        self.left_counter = 0
        self.right_counter = 0
        self.left_total = 0
        self.right_total = 0

    def eye_aspect_ratio(self, left_eye, right_eye):
        A = dist.euclidean(left_eye[1], left_eye[5])
        B = dist.euclidean(left_eye[2], left_eye[4])
        C = dist.euclidean(left_eye[0], left_eye[3])
        D = dist.euclidean(right_eye[1], right_eye[5])
        E = dist.euclidean(right_eye[2], right_eye[4])
        F = dist.euclidean(right_eye[0], right_eye[3])

        self.left_ear = (A + B) / (2.0 * C)
        self.right_ear = (D + E) / (2.0 * F)

    def detect_blink(self, morse_arr):
        if self.left_ear < self.EYE_AR_THRESH:
            self.left_counter += 1
        if self.right_ear < self.EYE_AR_THRESH:
            self.right_counter += 1
        else:
            if self.left_counter >= self.AR_CONSEC_FRAMES:
                self.left_total += 1
                morse_arr.append(".")
            if self.right_counter >= self.AR_CONSEC_FRAMES:
                self.right_total += 1
                morse_arr.append("-")
            self.left_counter = 0
            self.right_counter = 0
