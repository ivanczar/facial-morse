import argparse
import configparser
import time

import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream

from eyes import Eyes
from graphics_helper import GraphicsHelper
from mouth import Mouth
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

eyes = Eyes(blink_config)
mouth = Mouth(blink_config, eyes)
gh = GraphicsHelper(FRAME_WIDTH, eyes, mouth)
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
        leftEyeShape = shape[lStart:lEnd]
        rightEyeShape = shape[rStart:rEnd]
        mouthShape = shape[mStart:mEnd]

        eyes.eye_aspect_ratio(leftEyeShape, rightEyeShape)
        mouth.mouth_aspect_ratio(mouthShape)

        gh.draw_eyes_mouth(leftEyeShape, rightEyeShape, mouthShape, frame)

        # TODO: implement checkword

        eyes.detect_blink(morse_arr)
        mouth.detect_mouth(english_arr, morse_arr, random_word)

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
