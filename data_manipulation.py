import json


def add_word(chosen_words: dict, all_words: dict, required_word: str) -> str:
    """
    Adds required_word into chosen words.
    When required_word is already in chosen_words or when required_word is not
    in selected dictionary the function returns an informative message.
    :rtype: str
    :param chosen_words: dictionary, contains words which the user wants to
    learn
    :param all_words: dictionary, words from used dictionary
    :param required_word: str, word which the user wants to add into
    chosen_words
    :return: message about (un)successful addition
    """

    # White characters are stripped from required_word
    required_word.strip()

    # When required word contents empty string or only white characters,
    # the user is informed and is asked to enter some word
    if not required_word:
        return "Add some word."

    # It is searched by keys
    # When the word is already in MY VOCABULARY, the user is informed
    # by a message and is asked to enter another word
    elif required_word in chosen_words:
        return("This word has been already added. "
               "Try adding another word.")

    # Successfully addition is announced
    elif required_word in all_words:
        chosen_words[required_word] = all_words[required_word]
        return "The word has been successfully added."

    else:
        # When the word is not in selected dictionary,
        # the user is informed by a message
        return("This word is not in used dictionary. "
               "Try adding another word.")


def delete_word(chosen_words: dict, required_word: str) -> str:
    """
    Deletes required_word from chosen_words.
    :rtype: str
    :param chosen_words: contains words which the user wants to learn
    :param required_word: word which the user wants to delete from chosen_words
    :return: message about (un)successful deletion
    """

    # White characters are stripped from required_word
    required_word.strip()

    # It is searched by keys
    # When the required_word is in chosen_words, required_word is deleted
    if required_word in chosen_words:
        del chosen_words[required_word]
        return "This word has been successfully deleted."

    # When required word contains empty string or only white characters,
    # the user is informed and is asked to enter some word
    if not required_word:
        return "Write the word which you want to delete."

    else:
        # When the word is not in selected dictionary, the user is informed
        # by a message and is asked to enter another word
        return("This word is not in MY VOCABULARY. "
               "Try deleting another word.")


def delete_selected(chosen_words: dict, required_words: str) -> str:
    """
    Deletes all required_words from chosen_words.
    :rtype: str
    :param chosen_words: contains words which the user wants to learn
    :param required_words: words which the user wants to delete from chosen_words
    :return: message about (un)successful deletion
    """

    # When there are no chosen_words, the user is informed
    if not chosen_words:
        return "There are no words in MY VOCABULARY."

    # Variable required contains number of deleted words
    required = 0

    for required_word in required_words:

        # It is searched by keys
        # All required_words are deleted
        # After deletion of each word 1 point is added to variable required
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


def load_mv() -> dict:
    """
    Loads chosen_words.
    In the case there are no saved chosen_words,
    it is created new empty dictionary chosen_words.
    :rtype: dict
    :return: chosen_words: dict, contains words which the user wants to learn
    """

    # When there is no dictionary chosen_words, block try-except prevents
    # crashing in case of Exception
    try:
        # When there is saved chosen_words, it is loaded
        with open('save_mv.txt', encoding='utf-8') as saved:
            chosen_words = json.loads(saved.read())

    # In such case new empty dictionary chosen_words is created
    except FileNotFoundError:
        chosen_words = {}

    return chosen_words


def save_mv(chosen_words: dict) -> None:
    """
    Saves chosen_words to the disk.
    :param chosen_words: dict, contains words which the user wants to learn
    """

    with open('save_mv.txt', mode='w', encoding='utf-8') as saved:
        saved_vocabulary = json.dumps(chosen_words)
        print(saved_vocabulary, file=saved)