import pytest
from my_vocabulary import AllWords


all_words = AllWords()


@pytest.mark.parametrize("word", ["koupit", "být", "postavit"])
def test_search_successfully(word):
    assert all_words.search(word) is True


@pytest.mark.parametrize("word", ["3", "ahoj", "nos", ""])
def test_search_unsuccessfully(word):
    assert all_words.search(word) is False


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_value(key):
    assert all_words.value(key) == all_words.content[key]