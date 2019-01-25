from flask import Flask, render_template, request
from dictionary import load_dictionary
from data_manipulation import load_mv, add_word, delete_word, \
    delete_selected, save_mv
from learning import prepare_learning, guess_word, all_learned, \
    prepare_next_round

# At the beginning some global variables are set
all_words = load_dictionary()
chosen_words = load_mv()
learning_state = None
learning_stats = None

# Creates a Flask application
app = Flask(__name__)


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

    message = None
    message_mv = None

    # When user enters some word via writing the word into text input
    # and pressing submit Enter word, function add_word is executed
    # and the user is informed by a message
    if "add" in request.args:
        message = add_word(chosen_words, all_words, request.args['word'])

    # When user enters some word via writing the word into text input
    # and pressing submit Delete word, function delete_word is executed
    # and the user is informed by a message
    elif "delete" in request.args:
        message = delete_word(chosen_words, request.args['word'])

    # When user marks some words and presses submit Delete, function
    # delete_selected is executed and the user is informed by a message
    elif "delete_selected" in request.args:
        message_mv = delete_selected(chosen_words,
                                  request.args.getlist('select'))

    # After each statement chosen_words are saved.
    save_mv(chosen_words)


    # When there are no words in chosen_words, the user is informed
    # by a message
    if not chosen_words:
        message = "MY VOCABULARY is empty. Enter some words."

    return render_template(
        'administration.html',
        message=message,
        message_mv=message_mv,
        chosen_words=chosen_words
        )


@app.route('/learning/')
def learning():
    """
    Manages the process of learning.
    """

    # Some variables are prepared
    global learning_state, learning_stats
    message = None
    result = None
    is_done = None
    guess = None
    successful = None
    unsuccessful = None

    # When there are no words in chosen_words, the user is informed
    # by a message and the function ends
    if not chosen_words:
        message = "MY VOCABULARY is empty. Add some words."

    else:
        # No learning_state means, that the user is at the beginning
        # of his learning
        # The function prepare_learning is called and the variables
        # learning_state and learning_stats are prepared for learning
        if not learning_state:
                learning_state, learning_stats = prepare_learning(chosen_words)

        # When the user wants to continue with learning
        if 'continue' in request.args:

            # Ordered word from previous learning is deleted
            del learning_stats['ordered_words'][0]

            # When there are no more words in ordered_words
            if not learning_stats['ordered_words']:

                # It is checked, if all words are learned (if there were
                # any mistakes in the previous round)
                message, successful, unsuccessful = all_learned(learning_stats)

                # When all words are not learned yet, empty list means
                # that current round is at the end and it is necessary to
                # prepare next round
                if not message:
                    learning_state, learning_stats = prepare_next_round(
                        learning_state, learning_stats)

                # In this case learning is done
                # The function ends and variables learning_state
                # and learning_stats are prepared for next learning
                else:
                    learning_state = None
                    learning_stats = None
                    # When variable is_done is True, learning is done
                    is_done = True

        # New ordered word is prepared
        if not is_done:
            guess = learning_stats['ordered_words'][0]

        # The user enters guessed word
        # The function guess_word checks success or failure of the user
        # and returns the result and changed values of learning_state
        # and learning_stats
        if 'enter-guessed' in request.args:
            guessed = request.args['guessed']
            result, learning_state, learning_stats = guess_word(
                guess,
                guessed,
                learning_state,
                learning_stats
            )

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
    app.run(debug=True)



