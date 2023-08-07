# detect each individual facial expression (https://pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)

import argparse
import time

import cv2
import dlib
import imutils
import numpy as np
from imutils import face_utils
from imutils.video import VideoStream
from scipy.spatial import distance as dist

from randomwords import getWordDict

EYE_AR_THRESH = 0.25
MOUTH_AR_THRESH = 0.7
FRAME_WIDTH = 750
AR_CONSEC_FRAMES = 5

RANDOM_WORD = getWordDict()
COLORS = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]

LEFT_EYE_COUNTER = 0
RIGHT_EYE_COUNTER = 0
MOUTH_COUNTER = 0

LEFT_EYE_TOTAL = 0
RIGHT_EYE_TOTAL = 0
MOUTH_TOTAL = 0

MORSE_ARR = []
ENGLISH_ARR = []

MODE = "Freestyle"

ap = argparse.ArgumentParser()
ap.add_argument(
    "-p", "--shape-predictor", required=True, help="path to facial landmark predictor"
)
args = vars(ap.parse_args())


def morse_to_english(morse_arr, english_arr):
    map = {
        ".-": "A",
        "-...": "B",
        "-.-.": "C",
        "-..": "D",
        ".": "E",
        "..-.": "F",
        "--.": "G",
        "....": "H",
        "..": "I",
        ".---": "J",
        "-.-": "K",
        ".-..": "L",
        "--": "M",
        "-.": "N",
        "---": "O",
        ".--.": "P",
        "--.-": "Q",
        ".-.": "R",
        "...": "S",
        "-": "T",
        "..-": "U",
        "...-": "V",
        ".--": "W",
        "-..-": "X",
        "-.--": "Y",
        "--..": "Z",
    }
    morse_letter = "".join(morse_arr)
    if morse_letter in map:
        english_arr.append(map[morse_letter])
    else:
        morse_arr.clear()


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[2], mouth[10])
    B = dist.euclidean(mouth[4], mouth[8])
    C = dist.euclidean(mouth[0], mouth[6])
    mar = (A + B) / (2.0 * C)
    return mar


def detect_blink(
    eye_aspect_ratio, EAR_THRESH, eye_counter, eye_total, consec_frames, blink_char
):
    if eye_aspect_ratio < EAR_THRESH:
        eye_counter += 1
    else:
        if eye_counter >= consec_frames:
            eye_total += 1
            MORSE_ARR.append(blink_char)
        eye_counter = 0
    return eye_counter, eye_total


def detect_mouth(
    mouth_aspect_ratio,
    MOUTH_AR_THRESH,
    mouth_counter,
    mouth_total,
    left_total,
    right_total,
):
    if mouth_aspect_ratio > MOUTH_AR_THRESH:
        mouth_counter += 1
    else:
        if mouth_counter >= AR_CONSEC_FRAMES:
            if left_total == 0 and right_total == 0 and ENGLISH_ARR:
                ENGLISH_ARR.pop()
                mouth_total = 0
            else:
                mouth_total += 1
                left_total = 0
                right_total = 0
                morse_to_english(MORSE_ARR, ENGLISH_ARR)
                MORSE_ARR.clear()
        mouth_counter = 0
    return mouth_counter, mouth_total, left_total, right_total


def color_individual_letters(img, text, position, font_face, font_scale):
    x, y = position
    for letter, color in text.items():
        cv2.putText(img, letter, (x, y), font_face, font_scale, color, thickness=2)
        x += cv2.getTextSize(letter, font_face, font_scale, thickness=2)[0][0]


print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

print("[INFO] starting video stream thread...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
fileStream = False
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
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        mar = mouth_aspect_ratio(mouth)

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        mouthHull = cv2.convexHull(mouth)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

        LEFT_EYE_COUNTER, LEFT_EYE_TOTAL = detect_blink(
            leftEAR,
            EYE_AR_THRESH,
            LEFT_EYE_COUNTER,
            LEFT_EYE_TOTAL,
            AR_CONSEC_FRAMES,
            ".",
        )
        RIGHT_EYE_COUNTER, RIGHT_EYE_TOTAL = detect_blink(
            rightEAR,
            EYE_AR_THRESH,
            RIGHT_EYE_COUNTER,
            RIGHT_EYE_TOTAL,
            AR_CONSEC_FRAMES,
            "-",
        )
        MOUTH_COUNTER, MOUTH_TOTAL, LEFT_EYE_TOTAL, RIGHT_EYE_TOTAL = detect_mouth(
            mar,
            MOUTH_AR_THRESH,
            MOUTH_COUNTER,
            MOUTH_TOTAL,
            LEFT_EYE_TOTAL,
            RIGHT_EYE_TOTAL,
        )

        cv2.putText(
            frame,
            "L: {}".format(LEFT_EYE_TOTAL),
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "R: {}".format(RIGHT_EYE_TOTAL),
            (80, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "M: {}".format(MOUTH_TOTAL),
            (150, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "MORSE: {}".format("".join(MORSE_ARR)),
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "ENGLISH: {}".format("".join(ENGLISH_ARR)),
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )

        cv2.putText(
            frame,
            "L-EAR: {:.2f}".format(leftEAR),
            (FRAME_WIDTH - 150, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )
        cv2.putText(
            frame,
            "R-EAR: {:.2f}".format(leftEAR),
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

        color_individual_letters(
            frame, RANDOM_WORD, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 2
        )
    cv2.imshow("Frame", frame)
    cv2.setWindowTitle("Frame", "Facial Morse | " + MODE)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("l"):
        MODE = "Learning"
    if key == ord("q"):
        break
cv2.destroyAllWindows()
vs.stop()
