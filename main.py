# TODO: instantiate classes
# TODO: define configs

"""
TODO: QUESTIONS
Should i instantiate all objects (eye,mouth,graphics-helper) in main and pass them into App class?
    Should videostream, detector, and predictor be created in App or in main and passed into App?
Difference between passing into class constructor and then using self. within class methods vs just passing object as argument to method (i.e pass eyes object to detect_mouth instead of passing to constructor of Mouth)

Anything else i could improve on structure-wise?
"""
import argparse
import configparser

from app import App

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

app = App(blink_config, args, 750)
app.start()
