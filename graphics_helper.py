import cv2


class GraphicsHelper:
    def __init__(self, frame_width):
        self.blue_color = (255, 0, 0)
        self.green_color = (0, 255, 0)
        self.red_color = (0, 0, 255)
        self.grey_color = (129, 129, 129)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.color = self.red_color
        self.thickness = 2
        self.FRAME_WIDTH = frame_width

    def draw_eyes_mouth(self, left_eye_hull, right_eye_hull, mouth_hull, frame):
        cv2.drawContours(frame, [left_eye_hull], -1, self.green_color, 1)
        cv2.drawContours(frame, [right_eye_hull], -1, self.green_color, 1)
        cv2.drawContours(frame, [mouth_hull], -1, self.green_color, 1)

    def draw_hud(
        self,
        frame,
        left_eye_total,
        right_eye_total,
        mouth_total,
        morse_arr,
        english_arr,
        left_ear,
        right_ear,
        mar,
        FRAME_WIDTH,
    ):
        cv2.putText(
            frame,
            "L: {}".format(left_eye_total),
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "R: {}".format(right_eye_total),
            (80, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "M: {}".format(mouth_total),
            (150, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "MORSE: {}".format("".join(morse_arr)),
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "ENGLISH: {}".format("".join(english_arr)),
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

        cv2.putText(
            frame,
            "L-EAR: {:.2f}".format(left_ear),
            (FRAME_WIDTH - 150, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "R-EAR: {:.2f}".format(right_ear),
            (FRAME_WIDTH - 150, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "MAR: {:.2f}".format(mar),
            (FRAME_WIDTH - 150, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

    def color_individual_letters(self, img, random_word, position):
        x, y = position
        color_code = ()
        for i, letter in enumerate(random_word.word):
            match random_word.color_bool_array[i]:
                case True:
                    color_code = self.green_color
                case False:
                    color_code = self.red_color
                case None:
                    color_code = self.grey_color
            cv2.putText(
                img,
                letter,
                (x, y),
                self.font,
                self.font_scale,
                color_code,
                self.thickness,
            )
            x += cv2.getTextSize(letter, self.font, self.font_scale, thickness=2)[0][0]
