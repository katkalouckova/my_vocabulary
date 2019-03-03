from flask import Flask, render_template, request
import json
from my_vocabulary import MyVocabulary
from learning import LearningState, LearningProcess
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

    message = None
    result = None
    is_done = None
    guess = None
    successful = None
    unsuccessful = None

    my_vocabulary = MyVocabulary()
    learning_state = LearningState(my_vocabulary)
    learning_process = LearningProcess(learning_state)

    # No chosen_words
    if not my_vocabulary.chosen_words:
        message = "MY VOCABULARY is empty. Add some words."

    # User wants to continue with learning
    if 'continue' in request.args:
        # Ordered word from previous guessing is deleted
        learning_state.delete_first_ordered_word()

        # No more ordered_words
        if not learning_state.ordered_words:

            # Check, if is all learned
            if learning_process.is_all_learned():
                successful, unsuccessful = learning_process.get_result()
                message = "Good job! You already know all words!"
                is_done = True
                # TODO move message about (un)successful attempts from HTML
                learning_state = learning_state.reset_learning_state()

            else:
                # Next round
                learning_process.prepare_next_round()

    if not is_done:
        # New ordered_word
        guess = learning_process.get_offered_word()

    # The user enters guessed word
    if 'enter-guessed' in request.args:
        guessed = request.args['guessed']
        guessed.strip()

        # Word is guessed
        if learning_process.check_guessing(guess, guessed):
            learning_process.increment_success_counter()
            result = f'Right! Translation of "{guess}" is "{guessed}".'

        else:
            # Not guessed
            learning_process.increment_fail_counters(guess)
            result = f'Wrong! Correct translation of "{guess}" is' \
                     f' "{learning_state.words[guess]["value"]}".'

    return render_template(
        'learning.html',
        message=message,
        is_done=is_done,
        result=result,
        guess=guess,
        successful=successful,
        unsuccessful=unsuccessful
        )


# Run the application if executed as main package
if __name__ == '__main__':
    # Run in debug mode
    app.run(debug=True, host='0.0.0.0')
