import json
from constant import AGREE, DISAGREE
from util import clean


def enter_word(chosen_words, all_words):
    """
    The user enters words which he wants to learn.
    When the word is not in selected dictionary the user is asked to do it
    again until he chooses right word.
    """

    stay = "Y"

    while stay != "N":
        # The user enters word which he wants to learn
        # White characters are stripped
        required_word = input("Write the word which you want to add to MY "
                              "VOCABULARY: ").strip()

        # It is searched by keys
        # Successfully entering is announced and
        # When the word already is in MY VOCABULARY or is not in selected
        # dictionary, the user is informed by a message and is asked to
        # enter another word
        if required_word in chosen_words:
            print("This word has been already entered. "
                  "Try entering another word.\n")
        elif required_word in all_words:
            chosen_words[required_word] = all_words[required_word]
            print("The word has been successfully entered.\n")
        elif required_word not in all_words:
            print("This word is not in used dictionary. "
                  "Try entering another word.\n")

        stay = "Y"

        # Possibility to leave entering
        while stay not in ["", "N"]:
            stay = input('If you want to continue entering, press enter.\n'
                         'Otherwise press "N" and enter. \n')

            # The string is cleaned from white characters and is upppered
            stay = clean(stay)

        print()

    return chosen_words, all_words


def show_mv(chosen_words):
    """
    All words from MY VOCABULARY (from chosen_words) are printed
    """

    if not chosen_words:
        print("\nThere are no words in MY VOCABULARY.\n")
    else:
        print("\nMY VOCABULARY\n")
        for key, value in chosen_words.items():
            print(f"{key}: {value}")
        print()


def delete_word(chosen_words):
    """
    The user deletes words which he doesn't want to learn from MY VOCABULARY
    (from chosen_words)
    """
    stay = "Y"

    while stay != "N":
        # The user enters word which he wants to delete
        # White characters are stripped
        required_word = input("Write the word which you want to delete from "
                              "MY VOCABULARY: ").strip()

        # It is searched by keys
        # When the word already is in MY VOCABULARY or is not in selected
        # dictionary, the user is informed by a message and is asked to
        # enter another word
        if not chosen_words:
            print()
        elif required_word in chosen_words:
            del chosen_words[required_word]
            print("This word has been successfully deleted.\n")
        elif required_word not in chosen_words:
            print("This word is not in MY VOCABULARY. "
                  "Try deleting another word.\n")

        stay = "Y"

        # Possibility to leave deleting
        while stay not in ["", "N"]:
            stay = input('If you want to continue deleting, press enter.\n'
                         'Otherwise press "N" and enter.\n')

            # The string is cleaned from white characters and is upppered
            stay = clean(stay)

        print()

    return chosen_words


def delete_all(chosen_words):
    """
    The user deletes all words from MY VOCABULARY (from chosen_words)
    """

    confirmation = None

    while confirmation not in DISAGREE:
        # The user confirms deleting of all words from MY VOCABULARY
        # (from chosen_words)
        # White characters are stripped
        confirmation = input("Do you really want to delete all? "
                             'Write "Y" (yes) or "N" (no):\n')

        # The string is cleaned from white characters and is upppered
        confirmation = clean(confirmation)

        if confirmation in AGREE:
            chosen_words.clear()
            print("All words from MY VOCABULARY have been successfully "
                  "deleted.\n")
            break
        elif confirmation not in AGREE:
            input('Please answer "Y" or "N". \n')

    return chosen_words


def load_mv():
    """
    Chosen_words are loaded.
    In the case there are no saved chosen_words,
    it is created empty dictionary chosen_words.
    """

    try:
        with open('save_mv.txt', encoding='utf-8') as saved:
                chosen_words = json.loads(saved.read())

    except FileNotFoundError:
        chosen_words = {}

    return chosen_words


def save_mv(chosen_words):
    """
    Before leaving the program are words from MY VOCABULARY saved
    to save_mv.txt.
    """

    with open('save_mv.txt', mode='w', encoding='utf-8') as saved:
        saved_vocabulary = json.dumps(chosen_words)
        print(saved_vocabulary, file=saved)