from unittest.mock import mock_open
import pytest
import builtins
from io import StringIO
from flexmock import flexmock
from my_vocabulary import MyVocabulary


def __prepare():
    return MyVocabulary()


def __mock():
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save_mv=lambda: None)


def __mock_and_prepare():
    __mock()
    return __prepare()


def test_load_mv():
    flexmock(builtins).should_receive('open').and_return(StringIO('{"fake'
                                                                  '":"fake"}'))
    faked_vocabulary = __prepare()
    assert faked_vocabulary.chosen_words == {"fake": "fake"}


def test_create_mv():
    flexmock(builtins).should_receive('open').and_raise(FileNotFoundError)
    faked_vocabulary = MyVocabulary()
    assert faked_vocabulary.chosen_words == {}


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_word_is_in_mv(key):
    my_vocabulary = __mock_and_prepare()
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    assert my_vocabulary.word_is_in_mv(key) is True


@pytest.mark.parametrize("key", ["mluvit", "číst", "dům"])
def test_word_is_not_in_mv(key):
    my_vocabulary = __mock_and_prepare()
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    assert my_vocabulary.word_is_in_mv(key) is False


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_add_word(key):
    my_vocabulary = __mock_and_prepare()
    # Chosen_words is empty
    my_vocabulary.chosen_words = {}
    my_vocabulary.add_word(key)
    assert key in my_vocabulary.chosen_words


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_delete_word(key):
    my_vocabulary = __mock_and_prepare()
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    my_vocabulary.delete_word(key)
    assert key not in my_vocabulary.chosen_words


@pytest.mark.parametrize("key", [["koupit"], ["být"], ["postavit"]])
def test_delete_words_one_selected(key):
    my_vocabulary = __mock_and_prepare()
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    assert my_vocabulary.delete_words(key) == 1


@pytest.mark.parametrize("key", [["koupit", "být", "postavit"]])
def test_delete_words_three_selected(key):
    my_vocabulary = __mock_and_prepare()
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    assert my_vocabulary.delete_words(key) == 3


def test_save_mv():
    fake_file = mock_open(read_data='{}')
    flexmock(builtins, open=fake_file)
    my_vocabulary = __prepare()
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    my_vocabulary.save_mv()

    # Three following lines get what was written to the file
    string = ''
    for call in fake_file.return_value.write.mock_calls:
        string += (call[1][0])
    assert string == '{"koupit": "buy", "b\\u00fdt": "be", "postavit": ' \
                     '"build"}\n'
