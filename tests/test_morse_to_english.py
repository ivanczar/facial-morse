import pytest

from morse_to_english import morse_to_english


def test_success_conversion():
    morse_arr = [".", "-"]
    english_arr = []
    morse_to_english(morse_arr, english_arr)
    assert english_arr.__contains__("A")


def test_fail_conversion():
    morse_arr = [".", "-"]
    english_arr = []
    morse_to_english(morse_arr, english_arr)
    assert not english_arr.__contains__("B")


def test_invalid_conversion():
    morse_arr = [".", "-", ".", "-", ".", "-"]
    english_arr = []
    morse_to_english(morse_arr, english_arr)
    assert not english_arr
