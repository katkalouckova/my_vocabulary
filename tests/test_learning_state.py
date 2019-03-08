import builtins
import pytest
from flexmock import flexmock
from unittest.mock import mock_open
from learning import LearningState
from my_vocabulary import MyVocabulary


def __prepare():
    return LearningState(MyVocabulary())


def __mock():
    # Don't save changes in chosen_words
    flexmock(MyVocabulary, save_my_vocabulary=lambda: None)
    flexmock(LearningState, __del__=lambda: None)


def __mock_and_prepare():
    __mock()
    return __prepare()


@pytest.mark.parametrize("round_mistakes", [0, 3, 100])
def test_round_mistakes_clear(round_mistakes):
    learning_state = __mock_and_prepare()
    learning_state.round_mistakes_clear()
    assert learning_state.round_mistakes == 0


@pytest.mark.parametrize("successful", [0, 3, 100])
def test_increment_successful(successful):
    learning_state = __mock_and_prepare()
    n = learning_state.successful
    learning_state.increment_successful()
    assert learning_state.successful == n + 1


@pytest.mark.parametrize(["key", "value"],
                         [("koupit", "buy"),
                          ("být", "be"),
                          ("postavit", "build")],
                         )
def test_get_value(key, value):
    __mock()

    my_vocabulary = MyVocabulary()
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}

    learning_state = LearningState(my_vocabulary)
    learning_state.reset_learning_state()

    assert learning_state.get_value(key) == value


def test_get_unlearned():
    learning_state = __mock_and_prepare()

    util = {"koupit": False, "být": True, "postavit": False}

    # When there is something in learning_state.words, clear it
    learning_state.words = {}
    unlearned = []

    for word, learned in util.items():
        learning_state.words[word] = {'learned': learned}
        if learned is False:
            unlearned.append(word)

    assert learning_state.get_unlearned() == unlearned


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_set_learned(key):
    learning_state = __mock_and_prepare()

    util = {"koupit": False, "být": True, "postavit": False}

    # When there is something in learning_state.words, clear it
    learning_state.words = {}

    for word, learned in util.items():
        learning_state.words[word] = {'learned': learned}

    learning_state.set_learned(key)

    assert learning_state.words[key]['learned'] is True


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_total_mistakes(key):
    learning_state = __mock_and_prepare()

    util = {"koupit": 2, "být": 9, "postavit": 0}

    # When there is something in learning_state.words, clear it
    learning_state.words = {}

    for word, all_mistakes in util.items():
        learning_state.words[word] = {'total_mistakes': all_mistakes}

    assert learning_state.total_mistakes(key) == util[key]


def test_delete_first_ordered():
    learning_state = __mock_and_prepare()

    learning_state.ordered_words = ["koupit", "postavit"]
    learning_state.delete_first_ordered_word()

    assert learning_state.ordered_words == ["postavit"]


def test_get_learning_state():
    learning_state = __mock_and_prepare()

    learning_state.round_mistakes = 3
    learning_state.successful = 1
    learning_state.unsuccessful = 0
    learning_state.ordered_words = ["koupit", "postavit"]
    learning_state.words = {}
    
    result = learning_state.get_learning_state()
    
    assert result['round_mistakes'] == 3
    assert result['successful'] == 1
    assert result['unsuccessful'] == 0
    assert result['ordered_words'] == ["koupit", "postavit"]
    assert result['words'] == {}


def test_save_learning_state():
    # This file will be empty
    fake_file = mock_open(read_data='{}')
    # Function open returns fake_file
    flexmock(builtins, open=fake_file)

    # MyVocabulary and LearningState is not saved
    flexmock(MyVocabulary, save_my_vocabulary=lambda: None)
    my_vocabulary = MyVocabulary()
    # Setting my_vocabulary.chosen_words
    my_vocabulary.chosen_words = {"koupit": "buy"}

    flexmock(LearningState, __del__=lambda: None)
    # Setting learning_state with my_vocabulary.chosen_words
    learning_state = LearningState(my_vocabulary)

    learning_state.save_learning_state()

    string = ''
    for call in fake_file.return_value.write.mock_calls:
        string += (call[1][0])

    assert string == '{"round_mistakes": 0,' \
                     ' "successful": 0,' \
                     ' "unsuccessful": 0,' \
                     ' "ordered_words": ["koupit"],' \
                     ' "words": {' \
                     '"koupit": {"value": "buy", "learned": false,' \
                     ' "round_mistakes": 0, "total_mistakes": 0}}}\n'


def test_reset_learning_state():
    __mock()
    my_vocabulary = MyVocabulary()
    my_vocabulary.chosen_words = {"koupit": "buy"}
    learning_state = LearningState(my_vocabulary)
    learning_state.words['koupit']['learned'] = True

    learning_state.reset_learning_state()

    assert learning_state.words["koupit"]['learned'] is False
