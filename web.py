from flask import Flask, render_template, request
from dictionary import load_dictionary
from data_manipulation import load_mv, enter_word, delete_word, \
    delete_selected, save_mv
from learning_2 import prepare_learning, guess_word, all_learned, \
    prepare_next_round

# At the beginning are set some global variables
all_words = load_dictionary()
chosen_words = load_mv()
learning_state = None
learning_stats = None

# Command entered at the beginning of every flask application
app = Flask(__name__)


# Decorator with the function home() which is executed when user accesses
# homepage
@app.route('/')
def home():
    """
    Function home  returns render_template with the homepage.
    """
    return render_template('index.html')


@app.route('/administration/')
def admin():
    """
    Function admin contents possibilities, what can I do with my vocabulary:
        * enter words into my vocabulary (one word)
        * delete words from my vocabulary (one word)
        * delete selected words (one or more marked words)
    After each statement is my vocabulary saved.
    """

    message = None
    message_mv = None

    # When user enters some word via writing the word into text input
    # and pressing submit Enter word, is executed function enter_word
    # and the user is informed by a message
    if "enter" in request.args:
        message = enter_word(chosen_words, all_words, request.args['word'])

    # When user enters some word via writing the word into text input
    # and pressing submit Delete word, is executed function delete_word
    # and the user is informed by a message
    elif "delete" in request.args:
        message = delete_word(chosen_words, request.args['word'])

    # When user marks some words and presses submit Delete, is executed
    # function delete_selected and the user is informed by a message
    elif "delete_selected" in request.args:
        message_mv = delete_selected(chosen_words,
                                  request.args.getlist('select'))

    # After each statement are chosen_words saved.
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
    Function learning manages the process of learning.
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
        message = "MY VOCABULARY is empty. Enter some words."

    else:
        # No learning_state means, that the user is on the beginning
        # of his learning
        # It is called the function prepare_learning and the variables
        # learning_state and learning_stats are prepared for learning
        if not learning_state:
                learning_state, learning_stats = prepare_learning(chosen_words)

        # When the user wants to continue with learning
        if 'continue' in request.args:

            # Ordered word from previous learning is deleted
            del learning_stats['ordered_words'][0]

            # When there are no words more in ordered_words
            if not learning_stats['ordered_words']:

                # It is checked, if are all words learned (if in last round
                # were any mistakes)
                message, successful, unsuccessful = all_learned(learning_stats)

                # When all words are not learned, empty list means
                # that current round is at the end and it is necessary to
                # prepare next round
                if not message:
                    learning_state, learning_stats = prepare_next_round(
                        learning_state, learning_stats)

                # In this case is learned done
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


# Run in debug mode
if __name__ == '__main__':
    app.run(debug=True)



