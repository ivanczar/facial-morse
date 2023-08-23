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
FRAME_WIDTH = 750

app = App(blink_config, args, 750)
app.start()
