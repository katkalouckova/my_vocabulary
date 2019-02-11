from unittest.mock import mock_open
import pytest
import builtins
from io import StringIO
from flexmock import flexmock
from my_vocabulary import MyVocabulary, AllWords

my_vocabulary = MyVocabulary(AllWords())


def test_load_mv():
    flexmock(builtins).should_receive('open').and_return(StringIO('{"fake'
                                                                  '":"fake"}'))
    faked_vocabulary = MyVocabulary(AllWords())
    assert faked_vocabulary.chosen_words == {"fake": "fake"}


def test_create_mv():
    flexmock(builtins).should_receive('open').and_raise(FileNotFoundError)
    faked_vocabulary = MyVocabulary(AllWords())
    assert faked_vocabulary.chosen_words == {}


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_add_new_word(key):
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)
    # Chosen_words is empty
    my_vocabulary.chosen_words = {}
    added = my_vocabulary.add_word(key)
    assert added == "The word has been successfully added."


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_add_word_which_is_in_mv(key):
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)
    # In chosen_words are stated words, which I want to add
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    added = my_vocabulary.add_word(key)
    assert added == "This word has been already added. " \
                    "Try adding another word."


@pytest.mark.parametrize("key", ["mluvit", "číst", "dům"])
def test_add_word_not_in_dictionary(key):
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)
    # It doesn't matter, what is in chosen_words, so I don't set the state
    added = my_vocabulary.add_word(key)
    assert added == "This word is not in used dictionary. " \
                    "Try adding another word."


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_delete_word_successfully(key):
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    deleted = my_vocabulary.delete_word(key)
    assert deleted == "This word has been successfully deleted."


@pytest.mark.parametrize("key", ["foukat", "mluvit", "číst"])
def test_delete_word_unsuccessfully(key):
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    deleted = my_vocabulary.delete_word(key)
    assert deleted == "This word is not in MY VOCABULARY. " \
                      "Try deleting another word."


@pytest.mark.parametrize("key", [["koupit"], ["být"], ["postavit"]])
def test_delete_one_selected(key):
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    deleted_words = my_vocabulary.delete_selected(key)
    assert deleted_words == "Selected word has been successfully deleted."


@pytest.mark.parametrize("key", [["koupit", "být", "postavit"]])
def test_delete_three_selected(key):
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)
    # In chosen_words are all words, which I want to delete
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    deleted_words = my_vocabulary.delete_selected(key)
    assert deleted_words == "3 words have been successfully deleted."


def test_save():
    fake_file = mock_open(read_data='{}')
    flexmock(builtins, open=fake_file)
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    my_vocabulary.save()

    # Three following lines get what was written to the file
    string = ''
    for call in fake_file.return_value.write.mock_calls:
        string += (call[1][0])
    assert string == '{"koupit": "buy", "b\\u00fdt": "be", "postavit": ' \
                     '"build"}\n '
