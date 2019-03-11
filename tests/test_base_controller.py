import pytest
from flask import Flask, request

from base_controller import BaseController


def prepare():
    return BaseController(request)


def test_is_in_args():
    app = Flask(__name__)
    with app.test_request_context('/fake?word=buy'):
        base_controller = prepare()
        assert base_controller.is_in_args('word') is True


def test_is_not_in_args():
    app = Flask(__name__)
    with app.test_request_context('/fake?word=buy'):
        base_controller = prepare()
        assert base_controller.is_in_args('successful') is False


def test_check_correct_input():
    app = Flask(__name__)
    with app.test_request_context('/fake?word=buy'):
        base_controller = prepare()
        assert base_controller.get_required_word('word') == 'buy'


def test_check_incorrect_input():
    app = Flask(__name__)
    with app.test_request_context('/fake?word='):
        base_controller = prepare()
        assert base_controller.get_required_word('word') is None


def test_get_required_words():
    app = Flask(__name__)
    with app.test_request_context('/fake?select=buy&select=build'):
        base_controller = prepare()
        assert base_controller.get_required_words() == ['buy', 'build']