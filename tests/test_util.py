import pytest
from util import check_input


@pytest.mark.parametrize("word", [2, "ahoj", "s", "ddd"])
def test_check_correct_input(word):
    assert check_input(word) == str(word)


@pytest.mark.parametrize("word", ["", None])
def test_check_incorrect_input(word):
    assert check_input(word) is None
