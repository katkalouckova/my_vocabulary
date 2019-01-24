import json
from constant import AGREE, DISAGREE
from util import clean


def enter_word(chosen_words, all_words, required_word):
    """
    Required_word is added to chosen words.
    When required_word already is in chosen_words or when required_word is not
    in selected dictionary the user is informed by a message.
    """

    # White characters from required_word are stripped
    required_word.strip()

    # When required word contents empty string or only white characters,
    # the user is informed and is asked to enter some word
    if not required_word:
        return "Enter some word."

    # It is searched by keys
    # When the word already is in MY VOCABULARY, the user is informed
    # by a message and is asked to enter another word
    elif required_word in chosen_words:
        return("This word has been already entered. "
               "Try entering another word.")

    # Successfully entering is announced
    elif required_word in all_words:
        chosen_words[required_word] = all_words[required_word]
        return "The word has been successfully entered."

    else:
        # When the word is not in selected dictionary,
        # the user is informed by a message
        return("This word is not in used dictionary. "
               "Try entering another word.")


def delete_word(chosen_words, required_word):
    """
    The user deletes words which he doesn't want to learn from MY VOCABULARY
    (from chosen_words)
    """

    # White characters from required_word are stripped
    required_word.strip()

    # It is searched by keys
    # When the word is in chosen_words, required word is deleted
    if required_word in chosen_words:
        del chosen_words[required_word]
        return "This word has been successfully deleted."

    # When required word contents empty string or only white characters,
    # the user is informed and is asked to enter some word
    if not required_word:
        return "Write the word which you want to delete."

    else:
        # When the word is not in selected dictionary, the user is informed
        # by a message and is asked to enter another word
        return("This word is not in MY VOCABULARY. "
               "Try deleting another word.")


def delete_selected(chosen_words, required_words):
    """
    Required_words are checked one by one, if they are in chosen_words
    Words which are not in this dictionary are added
    """

    # When there are no chosen_words, the user is informed
    if not chosen_words:
        return "There are no words in MY VOCABULARY."

    # Variable required contents count of deleted words
    required = 0

    for required_word in required_words:

        # It is searched by keys
        # All marked words are deleted
        # After deleting of each word is 1 point added to variable required
        if required_word in chosen_words:
            del chosen_words[required_word]
            required += 1

    # When there are no marked words, the user is informed by a message
    if required == 0:
        return "There are no selected words to delete."

    # When there is one word selected, the user is informed by a message
    elif required == 1:
        return "Selected word has been successfully deleted."

    # When there are more words selected, the user is informed by a message
    # The message contents also information about the count of deleted words
    elif required > 1:
        return f'{required} selected words have been successfully deleted.'


def load_mv():
    """
    Chosen_words are loaded.
    In the case there are no saved chosen_words,
    it is created new empty dictionary chosen_words.
    """

    # When there is no dictionary chosen_words, block try-except prevents
    # raising of Exception
    try:
        # When there is saved chosen_words, it is loaded
        with open('save_mv.txt', encoding='utf-8') as saved:
                chosen_words = json.loads(saved.read())

    # In this case is created new empty dictionary chosen_words
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