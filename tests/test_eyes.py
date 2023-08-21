import configparser

import pytest

from eyes import Eyes


@pytest.fixture()
def eyes():
    config_data = configparser.ConfigParser()
    config_data.read("config.ini")
    blink_config = config_data["BLINK"]
    return Eyes(blink_config)


def test_short_blink(eyes):
    morse_arr = []
    eyes.ear = 0.26
    eyes.counter = 5
    eyes.detect_blink(morse_arr)
    assert "." in morse_arr


def test_long_blink(eyes):
    morse_arr = []
    eyes.ear = 0.26
    eyes.counter = 9
    eyes.detect_blink(morse_arr)
    assert "-" in morse_arr


def test_ear_thresh(eyes):
    morse_arr = []
    eyes.ear = 0.23
    eyes.counter = 5
    eyes.detect_blink(morse_arr)
    assert eyes.counter == 6
