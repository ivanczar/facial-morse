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
        self.is_learning = False
        self.is_easy = True
        self.random_word = RandomWord(self.is_easy)
        self.vs = VideoStream(src=0)
        self.morse_arr = []
        self.english_arr = []
        self.logger = Logger()

    def check_win_loss(self, frame):
        if self.random_word.get_green_count() == len(self.random_word.word):
            self.gh.display_win(frame)
            self.logger.log(f"WIN: {self.random_word.word}")
            self.logger.close()
        if self.random_word.get_red_count() >= 1:
            self.gh.display_loss(frame)
            self.logger.log(
                f"Loss: {self.random_word.word} (You entered {self.english_arr[len(self.english_arr) -1]} but needed {self.random_word.word[len(self.english_arr) -1]})"
            )
            self.logger.close()

    def check_word(self, frame):
        self.check_win_loss(frame)
        for i in range(len(self.english_arr)):
            if self.random_word.color_bool_array[i] is None:
                match (self.english_arr[i] == self.random_word.word[i]):
                    case True:
                        self.random_word.update_color_arr(i, True)
                        return
                    case False:
                        self.random_word.update_color_arr(i, False)
                        return

    def clear_arrays(self):
        self.morse_arr.clear()
        self.english_arr.clear()

    def toggle_mode(self):
        self.clear_arrays()
        self.is_learning = not self.is_learning

    def toggle_difficulty(self):
        self.is_easy = not self.is_easy
        self.reset_learning()

    def reset_learning(self):
        self.clear_arrays()
        self.random_word = RandomWord(self.is_easy)

    def start(self):
        print("[INFO] loading facial landmark predictor...")

        ######## Adapted from: https://pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/ ###
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
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                leftEyeShape = shape[lStart:lEnd]
                rightEyeShape = shape[rStart:rEnd]
                mouthShape = shape[mStart:mEnd]
                ##############################################################################
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
            if key == ord("d"):
                if self.is_learning:
                    self.toggle_difficulty()
            if key == ord("r"):
                if self.is_learning:
                    self.reset_learning()
                else:
                    self.clear_arrays()
            if key == ord("m"):
                self.toggle_mode()
            if key == ord("q"):
                break
        cv2.destroyAllWindows()
        self.logger.close()
        self.vs.stop()
