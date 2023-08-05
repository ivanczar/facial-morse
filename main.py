# detect each individual facial expression (https://pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)

# display translation in real time (of each letter or word at a time?)
# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

EYE_AR_THRESH = 0.19
MOUTH_AR_THRESH = 0.7

LEFT_EYE_COUNTER = 0
RIGHT_EYE_COUNTER = 0
MOUTH_COUNTER = 0

LEFT_EYE_TOTAL = 0
RIGHT_EYE_TOTAL = 0
MOUTH_TOTAL = 0
AR_CONSEC_FRAMES = 5

MORSE_ARR = []
ENGLISH_ARR = []



def morse_to_english(morse_arr, english_arr):
    map = {
        '.-': 'A',
        '-...': 'B',
        '-.-.': 'C',
        '-..': 'D',
        '.': 'E',
        '..-.': 'F',
        '--.': 'G',
        '....': 'H',
        '..': 'I',
        '.---': 'J',
        '-.-': 'K',
        '.-..': 'L',
        '--': 'M',
        '-.': 'N',
        '---': 'O',
        '.--.': 'P',
        '--.-': 'Q',
        '.-.': 'R',
        '...': 'S',
        '-': 'T',
        '..-': 'U',
        '...-': 'V',
        '.--': 'W',
        '-..-': 'X',
        '-.--': 'Y',
        '--..': 'Z',
    }
    morse_letter = "".join(morse_arr)
    if morse_letter in map:
        english_arr.append(map[morse_letter])
    else:
        morse_arr.clear()

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
args = vars(ap.parse_args())


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
    # if this is a file video stream, then we need to check if
    # there any more frames left in the buffer to process
    # if fileStream and not vs.more():
    #     break
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # detect faces in the grayscale frame
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
        # average the eye aspect ratio together for both eyes
        mar = mouth_aspect_ratio(mouth)

        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        mouthHull = cv2.convexHull(mouth)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
        def detect_blink(eye_aspect_ratio, EAR_THRESH, eye_counter, eye_total, consec_frames, blink_char):
            if eye_aspect_ratio < EAR_THRESH:
                eye_counter += 1
            else:
                if eye_counter >= consec_frames:
                    eye_total += 1
                    MORSE_ARR.append(blink_char)
                eye_counter = 0
            return eye_counter, eye_total


        def detect_mouth(mouth_aspect_ratio, MOUTH_AR_THRESH, mouth_counter, mouth_total, left_total, right_total):
            if mouth_aspect_ratio > MOUTH_AR_THRESH:
                mouth_counter += 1
            else:
                if mouth_counter >= AR_CONSEC_FRAMES:
                    mouth_total += 1
                    left_total = 0
                    right_total = 0
                    morse_to_english(MORSE_ARR, ENGLISH_ARR)
                    MORSE_ARR.clear()
                mouth_counter = 0
            return mouth_counter, mouth_total, left_total, right_total


        # Assuming you have computed the eye_aspect_ratio (leftEAR and rightEAR) and mouth_aspect_ratio (mar)
        LEFT_EYE_COUNTER, LEFT_EYE_TOTAL = detect_blink(leftEAR, EYE_AR_THRESH, LEFT_EYE_COUNTER, LEFT_EYE_TOTAL,
                                                        AR_CONSEC_FRAMES, ".")
        RIGHT_EYE_COUNTER, RIGHT_EYE_TOTAL = detect_blink(rightEAR, EYE_AR_THRESH, RIGHT_EYE_COUNTER, RIGHT_EYE_TOTAL,
                                                          AR_CONSEC_FRAMES, "-")
        MOUTH_COUNTER, MOUTH_TOTAL, LEFT_EYE_TOTAL, RIGHT_EYE_TOTAL = detect_mouth(mar, MOUTH_AR_THRESH, MOUTH_COUNTER, MOUTH_TOTAL, LEFT_EYE_TOTAL, RIGHT_EYE_TOTAL)
        # draw the total number of blinks on the frame along with
        # the computed eye aspect ratio for the frame
        cv2.putText(frame, "L: {}".format(LEFT_EYE_TOTAL), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "R: {}".format(RIGHT_EYE_TOTAL), (80, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "M: {}".format(MOUTH_TOTAL), (150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "MORSE: {}".format("".join(MORSE_ARR)), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "ENGLISH: {}".format("".join(ENGLISH_ARR)), (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(leftEAR), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(rightEAR), (600, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "MAR: {:.2f}".format(mar), (300, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
