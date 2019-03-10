from flask import Flask, request
from flexmock import flexmock
import builtins
import os

from my_vocabulary import MyVocabulary
from learning import LearningState, LearningProcess
from learning_controller import LearningController


def __mock():
    flexmock(MyVocabulary, save_my_vocabulary=lambda: None)
    flexmock(builtins)\
        .should_receive('open')\
        .and_raise(FileNotFoundError)
    flexmock(LearningState)\
        .should_receive('save_learning_state')\
        .and_return(None)


def __prepare():
    return LearningController(request)


def __mock_and_prepare():
    __mock()
    return LearningController(request)


def test_prepare_the_end():
    learning_controller = __mock_and_prepare()

    learning_controller.is_done = False

    flexmock(os)\
        .should_receive('remove')\
        .once()
    flexmock(LearningState)\
        .should_receive('reset_learning_state')\
        .once()
    flexmock(LearningProcess)\
        .should_receive('get_result')\
        .and_return((3, 2))

    learning_controller.prepare_the_end()

    assert learning_controller.is_done is True


def test_process_continue_next_round():
    learning_controller = __mock_and_prepare()

    learning_controller.learning_state.ordered_words = []

    flexmock(LearningState) \
        .should_receive('delete_first_ordered_word') \
        .once()
    flexmock(LearningProcess) \
        .should_receive('is_all_learned') \
        .and_return(False)
    flexmock(LearningProcess) \
        .should_receive('prepare_next_round') \
        .once()

    learning_controller.process_continue()


def test_process_continue_the_end():
    learning_controller = __mock_and_prepare()

    learning_controller.learning_state.ordered_words = []

    flexmock(LearningState) \
        .should_receive('delete_first_ordered_word') \
        .once()
    flexmock(LearningProcess) \
        .should_receive('is_all_learned') \
        .and_return(True)
    flexmock(LearningController) \
        .should_receive('prepare_the_end') \
        .once()

    learning_controller.process_continue()


def test_set_next_word():
    learning_controller = __mock_and_prepare()

    learning_controller.offered_word = None
    learning_controller.learning_state.ordered_words = ["koupit", "být",
                                                        "postavit"]

    learning_controller.set_next_word()

    assert learning_controller.offered_word == "koupit"


def test_set_answered_word():
    app = Flask(__name__)
    with app.test_request_context('/fake?answered_word=koupit'):
        learning_controller = __mock_and_prepare()

        learning_controller.set_answered_word()

        assert learning_controller.answered_word == "koupit"


def test_process_enter_answered_success():
    learning_controller = __mock_and_prepare()

    flexmock(LearningController)\
        .should_receive('set_answered_word')\
        .once()
    flexmock(LearningProcess)\
        .should_receive('check_guessing')\
        .and_return(True)
    flexmock(LearningProcess) \
        .should_receive('increment_success_counter') \
        .once()

    learning_controller.offered_word = "koupit"
    learning_controller.answered_word = "buy"

    learning_controller.process_enter_answered()

    assert learning_controller.result == 'Right! Translation of "koupit" is ' \
                                         '"buy".'


def test_process_enter_answered_fail():
    learning_controller = __mock_and_prepare()

    flexmock(LearningController) \
        .should_receive('set_answered_word') \
        .once()
    flexmock(LearningProcess) \
        .should_receive('check_guessing') \
        .and_return(False)
    flexmock(LearningProcess) \
        .should_receive('increment_fail_counters') \
        .once()
    learning_controller.offered_word = "koupit"
    learning_controller.learning_state.words["koupit"] = {"value": "buy"}

    learning_controller.process_enter_answered()

    assert learning_controller.result == 'Wrong! Correct translation of ' \
                                         '"koupit" is "buy".'


def test_handle_learning_controller_no_chosen_words():
    learning_controller = __mock_and_prepare()

    learning_controller.my_vocabulary.chosen_words = []

    learning_controller.handle_learning_controller()

    assert learning_controller.message == 'MY VOCABULARY is empty. Add some ' \
                                          'words.'


def test_handle_learning_controller_continue_next_word():
    app = Flask(__name__)
    with app.test_request_context('/fake?continue'):
        learning_controller = __mock_and_prepare()

        flexmock(LearningController)\
            .should_receive('process_continue')\
            .once()
        flexmock(LearningController)\
            .should_receive('set_next_word')\
            .once()

        learning_controller.my_vocabulary.chosen_words = {"koupit": "buy"}
        learning_controller.is_done = False

        learning_controller.handle_learning_controller()


def test_handle_learning_controller_enter_answered():
    app = Flask(__name__)
    with app.test_request_context('/fake?enter-answered='):
        learning_controller = __mock_and_prepare()

        flexmock(LearningController)\
            .should_receive('process_enter_answered')\
            .once()

        learning_controller.my_vocabulary.chosen_words = {"koupit": "buy"}
        learning_controller.is_done = True

        learning_controller.handle_learning_controller()

