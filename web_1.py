from flask import Flask, render_template, request
from my_vocabulary import MyVocabulary, AllWords
from util import check_input

app = Flask(__name__)

my_vocabulary = MyVocabulary(AllWords())


@app.route('/')
def home():
    """
    Creates a home page.
    """
    return render_template('index.html')


@app.route('/administration/')
def admin():
    """
    Creates an administration page.
    Admin page contains possibilities, what can I do with chosen_words:
        * enter words into my vocabulary (one word)
        * delete words from my vocabulary (one word)
        * delete selected words (one or more marked words)
    After each statement my vocabulary is saved.
    """

    # message above input type text
    message = None

    # message above table of MY VOCABULARY
    message_mv = None

    # The user pressed "Enter word" submit button
    if "add" in request.args:
        required_word = check_input(request.args['word'])

        if not required_word:
            message = "Add some word."
        else:
            message = my_vocabulary.add_word(required_word)

    # "Delete" submit button was pressed
    elif "delete" in request.args:
        required_word = check_input(request.args['word'])

        if not required_word:
            message = "Add some word."
        else:
            message = my_vocabulary.delete_word(required_word)

    # Some words were selected and submit button "Delete" was pressed
    elif "delete_selected" in request.args:
        required_words = request.args.getlist('select')

        if required_words:
            message_mv = my_vocabulary.delete_selected(required_words)
        else:
            message_mv = "There are no selected words to delete."

    # No words in MY VOCABULARY
    if not my_vocabulary.chosen_words:
        message = "MY VOCABULARY is empty. Enter some words."

    return render_template(
        'administration.html',
        message=message,
        message_mv=message_mv,
        chosen_words=my_vocabulary.chosen_words
        )
