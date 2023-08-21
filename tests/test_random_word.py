import pytest

from randomword import RandomWord


@pytest.fixture()
def easy_word():
    return RandomWord(True)


@pytest.fixture()
def difficult_word():
    return RandomWord(False)


def test_init_easy(easy_word):
    assert len(easy_word.word) == 4
    assert easy_word.color_bool_array.count(None) == 4


def test_init_difficult(difficult_word):
    assert len(difficult_word.word) == 8
    assert difficult_word.color_bool_array.count(None) == 8


def test_update_color(easy_word):
    assert easy_word.color_bool_array.count(None) == 4
    easy_word.update_color_arr(2, True)
    assert easy_word.color_bool_array.count(True) == 1
    assert easy_word.color_bool_array[2] == True
