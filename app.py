import argparse
import configparser
import time

import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream

from blinks import Blinks
from graphics_helper import GraphicsHelper
from randomword import RandomWord

ap = argparse.ArgumentParser()
ap.add_argument(
    "-p", "--shape-predictor", required=True, help="path to facial landmark predictor"
)
args = vars(ap.parse_args())

config_data = configparser.ConfigParser()
config_data.read("config.ini")
blink_config = config_data["BLINK"]
cv2_config = config_data["CV2"]

FRAME_WIDTH = 750

blinks = Blinks(blink_config)
gh = GraphicsHelper(FRAME_WIDTH, blinks)
random_word = RandomWord("easy")

morse_arr = []
english_arr = []


print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

print("[INFO] starting video stream thread...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(1.0)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=FRAME_WIDTH)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        # extract the left and right eye coordinates, then use the
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        mouth = shape[mStart:mEnd]

        blinks.eye_aspect_ratio(leftEye, rightEye)
        blinks.mouth_aspect_ratio(mouth)

        gh.draw_eyes_mouth(leftEye, rightEye, mouth, frame)

        # TODO: implement checkword

        blinks.detect_blink(morse_arr)
        blinks.detect_blink(morse_arr)
        blinks.detect_mouth(english_arr, morse_arr, random_word)

        gh.draw_hud(
            frame,
            FRAME_WIDTH,
            morse_arr,
            english_arr,
        )

        # gh.color_individual_letters(frame, random_word, (10,120))
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("p"):
        MODE = "Practice"
    if key == ord("q"):
        break
cv2.destroyAllWindows()
vs.stop()
