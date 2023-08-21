import math

import cv2


class GraphicsHelper:
    def __init__(self, frame_width, eyes, mouth):
        self.FRAME_WIDTH = frame_width
        self.blue_color = (255, 0, 0)
        self.green_color = (0, 255, 0)
        self.red_color = (0, 0, 255)
        self.grey_color = (129, 129, 129)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.color = self.red_color
        self.thickness = 2
        self.eyes = eyes
        self.mouth = mouth

    def draw_eyes_mouth(self, left_eye_shape, right_eye_shape, mouth_shape, frame):
        left_eye_hull = cv2.convexHull(left_eye_shape)
        right_eye_hull = cv2.convexHull(right_eye_shape)
        mouth_hull = cv2.convexHull(mouth_shape)
        cv2.drawContours(frame, [left_eye_hull], -1, self.green_color, 1)
        cv2.drawContours(frame, [right_eye_hull], -1, self.green_color, 1)
        cv2.drawContours(frame, [mouth_hull], -1, self.green_color, 1)

    def draw_hud(
        self,
        frame,
        morse_arr,
        english_arr,
    ):
        cv2.putText(
            frame,
            "Blinks: {}".format(self.eyes.total),
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        # cv2.putText(
        #     frame,
        #     "R: {}".format(self.eyes.right_total),
        #     (80, 30),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.7,
        #     (0, 0, 255),
        #     2,
        # )
        cv2.putText(
            frame,
            "M: {}".format(self.mouth.total),
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
            "EAR: {:.2f}".format(self.eyes.ear),
            (self.FRAME_WIDTH - 150, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

        cv2.putText(
            frame,
            "MAR: {:.2f}".format(self.mouth.mar),
            (self.FRAME_WIDTH - 150, 90),
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

    def display_win(self, frame):
        cv2.putText(
            frame,
            "You Win!!",
            (math.ceil(self.FRAME_WIDTH / 2), math.ceil(self.FRAME_WIDTH / 2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            2,
        )

    def display_loss(self, frame):
        cv2.putText(
            frame,
            "You Lost",
            (math.ceil(self.FRAME_WIDTH / 2), math.ceil(self.FRAME_WIDTH / 2)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 255),
            2,
        )
