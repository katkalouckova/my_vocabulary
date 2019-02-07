import pytest
from flexmock import flexmock
from my_vocabulary import MyVocabulary, AllWords


my_vocabulary = MyVocabulary(AllWords())


@pytest.mark.parametrize ("key", ["koupit", "být", "postavit"])
def test_add_new_word(key):
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)
    # Chosen_words is empty
    my_vocabulary.chosen_words = {}
    added = my_vocabulary.add_word(key)
    assert added == "The word has been successfully added."


@pytest.mark.parametrize ("key", ["koupit", "být", "postavit"])
def test_add_word_which_is_in_mv(key):
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save=lambda: None)
    # In chosen_words are stated words
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    added = my_vocabulary.add_word(key)
    assert added == "This word has been already added. " \
                    "Try adding another word."




