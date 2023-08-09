import argparse
import time

import cv2
import dlib
import imutils
import numpy as np
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
FRAME_WIDTH = 750

blinks = Blinks()
gh = GraphicsHelper(FRAME_WIDTH)
random_word = RandomWord("easy")

left_eye_counter = 0
right_eye_counter = 0
mouth_counter = 0

left_eye_total = 0
right_eye_total = 0
mouth_total = 0

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
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        mouth = shape[mStart:mEnd]
        leftEAR = blinks.eye_aspect_ratio(leftEye)
        rightEAR = blinks.eye_aspect_ratio(rightEye)
        mar = blinks.mouth_aspect_ratio(mouth)

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        mouthHull = cv2.convexHull(mouth)

        gh.draw_eyes_mouth(leftEyeHull, rightEyeHull, mouthHull, frame)

        left_eye_counter, left_eye_total = blinks.detect_blink(
            leftEAR, left_eye_counter, left_eye_total, ".", morse_arr
        )
        right_eye_counter, right_eye_total = blinks.detect_blink(
            rightEAR, right_eye_counter, right_eye_total, "-", morse_arr
        )
        (
            mouth_counter,
            mouth_total,
            left_eye_total,
            right_eye_total,
        ) = blinks.detect_mouth(
            english_arr,
            morse_arr,
            mar,
            random_word,
            mouth_total,
            mouth_counter,
            left_eye_total,
            right_eye_total,
        )
        gh.draw_hud(
            frame,
            left_eye_total,
            right_eye_total,
            mouth_total,
            morse_arr,
            english_arr,
            leftEAR,
            rightEAR,
            mar,
            FRAME_WIDTH,
        )
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("p"):
        MODE = "Practice"
    if key == ord("q"):
        break
cv2.destroyAllWindows()
vs.stop()
