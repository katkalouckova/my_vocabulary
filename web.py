from flask import Flask, render_template, request
from my_vocabulary import MyVocabulary, AllWords
from learning import LearningState, LearningProcess
from util import check_input

app = Flask(__name__)

my_vocabulary = MyVocabulary(AllWords())
learning_state = None
learning_process = None


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
    :return: render_template
    """

    # message above input type text
    message = None
    # message above table of MY VOCABULARY
    message_mv = None

    # The user pressed "Add word"
    if "add" in request.args:
        required_word = check_input(request.args['word'])

        # There is some input
        if required_word:

            # Check if tho word is in used dictionary
            if my_vocabulary.exists_word(required_word):

                # Successful addition
                if my_vocabulary.add_word(required_word):
                    message = "The word has been successfully added."

                else:
                    # Unsuccessful addition
                    message = "This word has been already added. " \
                              "Try adding another word."

            else:
                # Not in used dictionary
                message = "This word is not in used dictionary." \
                          "Try adding another word."

        else:
            # Nothing was entered
            message = "Enter some word."

    # "Delete" submit button was pressed
    elif "delete" in request.args:
        required_word = check_input(request.args['word'])

        # There is some input
        if required_word:
            # Successful deletion
            if my_vocabulary.delete_word(required_word):
                message = "This word has been successfully deleted."

            else:
                # Unsuccessful addition
                message = "This word is not in MY VOCABULARY. " \
                          "Try deleting another word."

        else:
            # Nothing was entered
            message = "Enter some word."

    # Some words were selected and submit button "Delete" was pressed
    elif "delete_selected" in request.args:
        required_words = request.args.getlist('select')

        # Successfully deletion
        if required_words:
            deleted = my_vocabulary.delete_selected(required_words)

            # One word deleted
            if deleted == 1:
                message_mv = "Selected word has been successfully deleted."

            # More words deleted
            elif deleted > 1:
                message_mv = f'{deleted} words have been successfully deleted.'
        else:
            # Nothing was selected
            message_mv = "There are no selected words to delete."

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

    global learning_state
    global learning_process

    # The instances are created only at the beginning of learning
    if not learning_state:
        learning_state = LearningState(my_vocabulary)
        learning_process = LearningProcess(learning_state)

    # No chosen_words
    if not my_vocabulary.chosen_words:
        message = "MY VOCABULARY is empty. Add some words."

    else:

        # User wants to continue with learning
        if 'continue' in request.args:
            # Ordered word from previous guessing is deleted
            learning_state.delete_first_ordered_word()

            # No more ordered_words
            if not learning_state.ordered_words:

                # Check, if is all learned
                if learning_process.check_all_learned():
                    successful, unsuccessful = learning_process.get_result()
                    message = "Good job! You already know all words!"
                    is_done = True
                    # TODO move message about (un)successful attempts from HTML
                    learning_state = learning_state.reset()

                else:
                    # Next round
                    learning_process.prepare_next_round()

        if not is_done:
            # New ordered_word
            guess = learning_process.guess()

        # The user enters guessed word
        if 'enter-guessed' in request.args:
            guessed = request.args['guessed']
            guessed.strip()

            # Word is guessed
            if learning_process.check_guessing(guess, guessed):
                learning_process.guessed()
                result = f'Right! Translation of "{guess}" is "{guessed}".'

            else:
                # Not guessed
                learning_process.not_guessed(guess)
                result = f'Wrong! Correct translation of "{guess}" is' \
                         f'"{learning_state.words[guess]["value"]}".'

    return render_template('learning.html',
                                       message=message,
                                       is_done=is_done,
                                       result=result,
                                       guess=guess,
                                       successful=successful,
                                       unsuccessful=unsuccessful)


# Run the application if executed as main package
if __name__ == '__main__':
    # Run in debug mode
    app.run(debug=True, host='0.0.0.0')
