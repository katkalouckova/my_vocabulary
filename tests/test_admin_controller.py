from flask import Flask, request
from flexmock import flexmock
import builtins

from my_vocabulary import MyVocabulary
from admin_controller import AdminController


def __mock():
    flexmock(MyVocabulary, save_my_vocabulary=lambda: None)
    flexmock(builtins).should_receive('open').and_raise(FileNotFoundError)


def __prepare():
    return AdminController(request)


def __mock_and_prepare():
    __mock()
    return AdminController(request)


def test_process_add_not_required_word():
    app = Flask(__name__)
    with app.test_request_context('/fake?word='):
        admin_controller = __mock_and_prepare()
        admin_controller.process_add()
        assert admin_controller.message == "Enter some word."


def test_process_add_not_in_dictionary():
    app = Flask(__name__)
    with app.test_request_context('/fake?word=jkl'):
        admin_controller = __mock_and_prepare()
        admin_controller.process_add()
        assert admin_controller.message == "This word is not in used " \
                                           "dictionary. Try adding another " \
                                           "word."


def test_process_add_word_is_in_mv():
    app = Flask(__name__)
    with app.test_request_context('/fake?word=koupit'):
        admin_controller = __mock_and_prepare()
        admin_controller.my_vocabulary.chosen_words = {"koupit": "buy",
                                                       "být": "be",
                                                       "postavit": "build"}
        admin_controller.process_add()
        assert admin_controller.message == "This word has been already added."\
                                           " Try adding another word."


def test_process_add_successfully():
    app = Flask(__name__)
    with app.test_request_context('/fake?word=foukat'):
        admin_controller = __mock_and_prepare()
        admin_controller.process_add()
        assert admin_controller.message == "The word has been successfully " \
                                           "added."


def test_process_delete_word_not_required_word():
    app = Flask(__name__)
    with app.test_request_context('/fake?word='):
        admin_controller = __mock_and_prepare()
        admin_controller.process_add()
        assert admin_controller.message == "Enter some word."


def test_process_delete_word_is_not_in_mv():
    app = Flask(__name__)
    with app.test_request_context('/fake?word=jkl'):
        admin_controller = __mock_and_prepare()
        admin_controller.my_vocabulary.chosen_words = {"koupit": "buy"}
        admin_controller.process_delete_word()
        assert admin_controller.message == "This word is not in MY " \
                                           "VOCABULARY. " \
                                           "Try deleting another word."


def test_process_delete_word_successfully():
    app = Flask(__name__)
    with app.test_request_context('/fake?word=koupit'):
        admin_controller = __mock_and_prepare()
        admin_controller.my_vocabulary.chosen_words = {"koupit": "buy"}
        admin_controller.process_delete_word()
        assert admin_controller.message == "This word has been successfully " \
                                           "deleted."


def test_process_delete_words_nothing_selected():
    app = Flask(__name__)
    with app.test_request_context('/fake?'):
        admin_controller = __mock_and_prepare()
        admin_controller.my_vocabulary.chosen_words = {"koupit": "buy",
                                                       "být": "be",
                                                       "postavit": "build"}
        admin_controller.process_delete_words()
        assert admin_controller.message_mv == "There are no selected words " \
                                              "to delete."


def test_process_delete_words_two_selected():
    app = Flask(__name__)
    with app.test_request_context('/fake?select=koupit&select=postavit'):
        admin_controller = __mock_and_prepare()
        admin_controller.my_vocabulary.chosen_words = {"koupit": "buy",
                                                       "být": "be",
                                                       "postavit": "build"}
        admin_controller.process_delete_words()
        assert admin_controller.message_mv == "Number of successfully " \
                                              "deleted words: 2"


def test_handle_admin_controller_add():
    app = Flask(__name__)
    with app.test_request_context('/fake?add='):
        admin_controller = __mock_and_prepare()
        flexmock(admin_controller).should_receive(
            'process_add').once()
        admin_controller.handle_admin_controller()


def test_handle_admin_controller_delete_word():
    app = Flask(__name__)
    with app.test_request_context('/fake?delete='):
        admin_controller = __mock_and_prepare()
        flexmock(admin_controller).should_receive(
            'process_delete_word').once()
        admin_controller.handle_admin_controller()


def test_handle_admin_controller_delete_words():
    app = Flask(__name__)
    with app.test_request_context('/fake?delete_words='):
        admin_controller = __mock_and_prepare()
        flexmock(admin_controller).should_receive(
            'process_delete_words').once()
        admin_controller.handle_admin_controller()


def test_handle_admin_controller_delete():
    app = Flask(__name__)
    with app.test_request_context('/fake?'):
        admin_controller = __mock_and_prepare()
        admin_controller.my_vocabulary.chosen_words = {}
        admin_controller.handle_admin_controller()
        assert admin_controller.message == "MY VOCABULARY is empty. " \
                                           "Enter some words."

