import time

import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream

from eyes import Eyes
from graphics_helper import GraphicsHelper
from logger import Logger
from mouth import Mouth
from randomword import RandomWord


class App:
    def __init__(self, blink_config, args, FRAME_WIDTH):
        self.FRAME_WIDTH = FRAME_WIDTH
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(args["shape_predictor"])
        self.eyes = Eyes(blink_config)
        self.mouth = Mouth(blink_config, self.eyes)
        self.gh = GraphicsHelper(FRAME_WIDTH, self.eyes, self.mouth)
        self.random_word = RandomWord("easy")
        self.vs = VideoStream(src=0)
        self.is_learning = False
        self.morse_arr = []
        self.english_arr = []
        # self.logger = Logger(self.random_word.word)

    def check_word(self, frame):
        if self.random_word.get_green_count() == len(self.random_word.word):
            self.gh.display_win(frame)

        for i in range(len(self.english_arr)):
            if self.random_word.color_bool_array[i] is None:
                match (self.english_arr[i] == self.random_word.word[i]):
                    case True:
                        self.random_word.update_color_arr(i, True)
                        return
                    case False:
                        self.random_word.update_color_arr(i, False)
                        # self.logger.update_errors()
                        print("HERE")
                        return

    def clear_arrays(self):
        self.morse_arr.clear()
        self.english_arr.clear()

    def toggle_mode(self):
        self.clear_arrays()
        self.is_learning = not self.is_learning

    def reset_learning(self):
        self.clear_arrays()
        self.random_word = RandomWord("easy")

    def start(self):
        print("[INFO] loading facial landmark predictor...")

        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

        print("[INFO] starting video stream thread...")
        self.vs.start()
        # vs = VideoStream(usePiCamera=True).start()
        time.sleep(1.0)

        while True:
            frame = self.vs.read()
            frame = imutils.resize(frame, width=self.FRAME_WIDTH)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = self.detector(gray, 0)
            for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                # extract the left and right eye coordinates, then use the
                leftEyeShape = shape[lStart:lEnd]
                rightEyeShape = shape[rStart:rEnd]
                mouthShape = shape[mStart:mEnd]

                self.eyes.eye_aspect_ratio(leftEyeShape, rightEyeShape)
                self.mouth.mouth_aspect_ratio(mouthShape)

                self.gh.draw_eyes_mouth(leftEyeShape, rightEyeShape, mouthShape, frame)

                self.eyes.detect_blink(self.morse_arr)
                self.mouth.detect_mouth(
                    self.english_arr, self.morse_arr, self.random_word
                )

                self.gh.draw_hud(
                    frame,
                    self.morse_arr,
                    self.english_arr,
                )

                if self.is_learning:
                    self.gh.color_individual_letters(frame, self.random_word, (10, 120))
                    self.check_word(frame)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("r") and self.is_learning:
                self.reset_learning()
            if key == ord("m"):
                self.toggle_mode()
            if key == ord("q"):
                break
        cv2.destroyAllWindows()
        self.vs.stop()
