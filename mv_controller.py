from data_manipulation import enter_word, show_mv, delete_word, delete_all
from util import clean


def handle_mv(chosen_words, all_words):
    """
    This menu leads the user to different functions which work
    with MY VOCABULARY
    """

    decision = None

    while decision not in ["Q", "H"]:
        # The user enters chosen letter according to what he wants to do
        decision = input('Write "E", if you want to enter new word.\n'
                         'Write "S", if you want to show all words '
                         'from MY VOCABULARY\n'
                         'Write "D", if you want to delete some word '
                         'from MY VOCABULARY.\n'
                         'Write "A", if you want to delete all words '
                         'from MY VOCABULARY.\n'
                         'Write "H", if you want to go to handle home menu.\n'
                         'Write "Q", if you want to quit the program.\n')

        # The string is cleaned from white characters and is upppered
        decision = clean(decision)

        # According to chosen letter is called proper function
        # When the user enters incorrect letter, he is informed by a message
        # and is asked to enter another letter
        if decision == "E":
            chosen_words, all_words = enter_word(chosen_words, all_words)
        elif decision == "S":
            show_mv(chosen_words)
        elif decision == "D":
            chosen_words = delete_word(chosen_words)
        elif decision == "A":
            chosen_words = delete_all(chosen_words)
        elif decision not in ["Q", "H"]:
            print('Choose one of offered possibilities. \n')

    return decision, chosen_words, all_words
