from flask import Flask, render_template, request
from my_vocabulary import MyVocabulary
from learning_controller import LearningController
from util import check_input

app = Flask(__name__)


@app.route('/')
def home():
    """
    Creates a home page.
    """
    return render_template('index.html')


@app.route('/administration/')
def administration():
    """
    Creates an administration page.
    Admin page contains possibilities, what can I do with chosen_words:
        * enter word into my vocabulary (one word)
        * delete word from my vocabulary (one word)
        * delete selected words (one or more selected words)
    After each statement my vocabulary is saved.
    :return: render_template
    """

    my_vocabulary = MyVocabulary()

    # message above input type text
    message = None
    # message above table of MY VOCABULARY
    message_mv = None

    # The user pressed "Add word"
    if "add" in request.args:
        required_word = check_input(request.args['word'])

        # Nothing was entered
        if not required_word:
            message = "Enter some word."

        # Not in used dictionary
        elif not my_vocabulary.word_is_in_dictionary(required_word):
            message = "This word is not in used dictionary." \
                      "Try adding another word."

        # Already in mv
        elif my_vocabulary.word_is_in_mv(required_word):
            message = "This word has been already added. " \
                      "Try adding another word."

        else:
            # Successful addition
            my_vocabulary.add_word(required_word)
            message = "The word has been successfully added."

    # "Delete" submit button was pressed
    elif "delete" in request.args:
        required_word = check_input(request.args['word'])

        # Nothing was entered
        if not required_word:
            message = "Enter some word."

        # Not in mv
        elif not my_vocabulary.word_is_in_mv(required_word):
            message = "This word is not in MY VOCABULARY. " \
                      "Try deleting another word."

        else:
            # Successful deletion
            my_vocabulary.delete_word(required_word)
            message = "This word has been successfully deleted."

    # Some words were selected and submit button "Delete" was pressed
    elif "delete_words" in request.args:
        required_words = request.args.getlist('select')

        # Nothing was selected
        if not required_words:
            message_mv = "There are no selected words to delete."

        else:
            # Successfully deletion
            deleted = my_vocabulary.delete_words(required_words)
            message_mv = f"Number of successfully deleted words: {deleted}"

    # No words in MY VOCABULARY
    if not message and not my_vocabulary.chosen_words:
        message = "MY VOCABULARY is empty. Enter some words."

    return render_template(
        'administration.html',
        message=message,
        message_mv=message_mv,
        chosen_words=my_vocabulary.chosen_words
        )


@app.route('/learning')
def learning():
    """
    Manages the process of learning.
    :return: render_template
    """

    learning_controller = LearningController(request)

    learning_controller.handle_learning_controller()

    return learning_controller.prepare_render_template()


# Run the application if executed as main package
if __name__ == '__main__':
    # Run in debug mode
    app.run(debug=True, host='0.0.0.0')
