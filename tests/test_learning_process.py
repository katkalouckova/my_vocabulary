import builtins
from unittest.mock import mock_open

import pytest
from flexmock import flexmock

from learning import LearningProcess, LearningState
from my_vocabulary import MyVocabulary


def __prepare():
    return LearningState(MyVocabulary())


def __mock():
    # Don't save changes
    flexmock(MyVocabulary, save_my_vocabulary=lambda: None)
    flexmock(LearningState, __del__=lambda: None)
    # This file will be empty
    fake_file = mock_open(read_data='{}')
    # Function open returns fake_file
    flexmock(builtins, open=fake_file)


def __mock_and_prepare():
    __mock()
    return __prepare()


@pytest.mark.parametrize(["offered_word", "answered_word"],
                         [("koupit", "buy"),
                          ("být", "be"),
                          ("postavit", "build")],
                         )
def test_check_guessing_successfully(offered_word, answered_word):
    __mock()
    my_vocabulary = MyVocabulary()
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}

    learning_process = LearningProcess(LearningState(my_vocabulary))

    assert learning_process.check_guessing(offered_word, answered_word)


@pytest.mark.parametrize(["offered_word", "answered_word"],
                         [("koupit", "koupit"),
                          ("být", "bee"),
                          ("postavit", "buil")],
                         )
def test_check_guessing_unsuccessfully(offered_word, answered_word):
    __mock()

    my_vocabulary = MyVocabulary()
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}

    flexmock(LearningState, __del__=lambda: None)
    learning_process = LearningProcess(LearningState(my_vocabulary)
                                       )
    assert not learning_process.check_guessing(offered_word, answered_word)


def test_increment_success_counter():
    learning_state = __mock_and_prepare()

    successful = learning_state.successful

    learning_process = LearningProcess(learning_state)
    learning_process.increment_success_counter()

    assert learning_state.successful == successful + 1


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_fail_counters(key):
    __mock()

    my_vocabulary = MyVocabulary()
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}

    learning_state = LearningState(my_vocabulary)
    total_m = learning_state.words[key]['total_mistakes']
    unsuccessful = learning_state.unsuccessful
    round_m = learning_state.round_mistakes

    learning_process = LearningProcess(learning_state)
    learning_process.increment_fail_counters(key)

    assert learning_state.words[key]['total_mistakes'] == total_m + 1
    assert learning_state.round_mistakes == round_m + 1
    assert learning_state.unsuccessful == unsuccessful + 1


def test_is_all_learned_true():
    learning_state = __mock_and_prepare()
    learning_state.round_mistakes = 0

    learning_process = LearningProcess(learning_state)

    assert learning_process.is_all_learned() is True


@pytest.mark.parametrize("number", [1, 10, 30])
def test_is_all_learned_false(number):
    learning_state = __mock_and_prepare()
    learning_state.round_mistakes = number

    learning_process = LearningProcess(learning_state)

    assert learning_process.is_all_learned() is False


def test_get_result():
    learning_state = __mock_and_prepare()
    learning_state.successful = 5
    learning_state.unsuccessful = 1

    learning_process = LearningProcess(learning_state)

    assert learning_process.get_result() == (5, 1)


def test_prepare_next_round():
    learning_state = __mock_and_prepare()

    learning_state.round_mistakes = 2
    learning_state.words = {"koupit": {"learned": False,
                                       "round_mistakes": 1,
                                       "total_mistakes": 2},
                            "být": {"learned": True,
                                    'round_mistakes': 0,
                                    "total_mistakes": 1},
                            "postavit": {"learned": False,
                                         'round_mistakes': 1,
                                         "total_mistakes": 2}}

    learning_process = LearningProcess(learning_state)
    learning_process.prepare_next_round()

    assert learning_state.round_mistakes == 0
    assert sorted(learning_state.ordered_words) == ["koupit", "koupit",
                                                    "postavit", "postavit"]
