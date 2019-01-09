from mv_controller import handle_mv
from learning import learning_mode
from util import clean


def handle_home(chosen_words, all_words):
    """
    First menu, leads to working with MY VOCABULARY, to learning or to exit
    """

    decision = None

    while decision != "Q":
        # The user enters chosen letter according to what he wants to do
        decision = input('Write "V", if you want to work with MY VOCABULARY.\n'
                         'Write "L", if you want to learn words.\n'
                         'Write "Q", if you want to quit the program.\n')

        # The string is cleaned from white characters and is upppered
        decision = clean(decision)

        # According to chosen letter is called proper function
        # When the user enters incorrect letter, he is informed by a message
        # and is asked to enter another letter
        if decision == "V":
            decision, chosen_words, all_words = handle_mv(chosen_words,
                                                          all_words)
        elif decision == "L":
            learning_mode(chosen_words)
        elif decision != "Q":
            print('Write "V", "L" or "Q".\n')

    return chosen_words, all_words

