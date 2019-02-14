from unittest.mock import mock_open
import pytest
import builtins
from io import StringIO
from flexmock import flexmock
from my_vocabulary import MyVocabulary, AllWords


def __prepare():
    return MyVocabulary(AllWords())


def __mock_and_prepare():
    __mock()
    return __prepare()


def __mock():
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)


def test_load_mv():
    flexmock(builtins).should_receive('open').and_return(StringIO('{"fake'
                                                                  '":"fake"}'))
    faked_vocabulary = __prepare()
    assert faked_vocabulary.chosen_words == {"fake": "fake"}


def test_create_mv():
    flexmock(builtins).should_receive('open').and_raise(FileNotFoundError)
    faked_vocabulary = MyVocabulary(AllWords())
    assert faked_vocabulary.chosen_words == {}


@pytest.mark.parametrize("key", ["začít", "kousnout", "foukat"])
def test_exists_word_in_dictionary(key):
    my_vocabulary = __mock_and_prepare()
    assert my_vocabulary.exists_word(key) is True


@pytest.mark.parametrize("key", ["mluvit", "číst", "dům"])
def test_exists_word_not_in_dictionary(key):
    my_vocabulary = __mock_and_prepare()
    assert my_vocabulary.exists_word(key) is False


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_add_new_word(key):
    my_vocabulary = __mock_and_prepare()
    # Chosen_words is empty
    my_vocabulary.chosen_words = {}
    assert my_vocabulary.add_word(key) is True


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_add_word_which_is_in_mv(key):
    my_vocabulary = __mock_and_prepare()
    # In chosen_words are stated words, which I want to add
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    assert my_vocabulary.add_word(key) is False


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_delete_word_successfully(key):
    my_vocabulary = __mock_and_prepare()
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    assert my_vocabulary.delete_word(key) is True


@pytest.mark.parametrize("key", ["foukat", "mluvit", "číst"])
def test_delete_word_unsuccessfully(key):
    my_vocabulary = __mock_and_prepare()
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    assert my_vocabulary.delete_word(key) is False


@pytest.mark.parametrize("key", [["koupit"], ["být"], ["postavit"]])
def test_delete_one_selected(key):
    my_vocabulary = __mock_and_prepare()
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    assert my_vocabulary.delete_selected(key) == 1


@pytest.mark.parametrize("key", [["koupit", "být", "postavit"]])
def test_delete_three_selected(key):
    my_vocabulary = __mock_and_prepare()
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    assert my_vocabulary.delete_selected(key) == 3


def test_save():
    fake_file = mock_open(read_data='{}')
    flexmock(builtins, open=fake_file)
    my_vocabulary = __prepare()
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    my_vocabulary.save()

    # Three following lines get what was written to the file
    string = ''
    for call in fake_file.return_value.write.mock_calls:
        string += (call[1][0])
    assert string == '{"koupit": "buy", "b\\u00fdt": "be", "postavit": ' \
                     '"build"}\n'
