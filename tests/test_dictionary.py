import pytest
from my_vocabulary import Dictionary


dictionary = Dictionary()


@pytest.mark.parametrize("word", ["koupit", "být", "postavit"])
def test_word_is_in_dictionary(word):
    assert dictionary.word_is_in_dictionary(word) is True


@pytest.mark.parametrize("word", ["3", "ahoj", "nos", ""])
def test_word_is_not_in_dictionary(word):
    assert dictionary.word_is_in_dictionary(word) is False


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_get_value(key):
    assert dictionary.get_value(key) == dictionary.content[key]
