from random import shuffle


def prepare_learning(chosen_words: dict) -> tuple:
    """
    Creates learning_state and learning_stats dictionaries.
    Dictionary learning_state is created from dictionary chosen_words.
    Each key from chosen_words is key of this dictionary and value contains
    dictionary with following three keys:
    * value (value from chosen_words),
    * learned (True or False),
    * all_mistakes (number of all mistakes during learning - each word)
    Another dictionary learning_stats is created. It is independent
    of particular words from chosen_words. It contains keys:
    * round_mistakes (number of mistakes during round - together}
    * successful (number of successful guessing attempts)
    * unsuccessful (number of unsuccessful attempts)
    :rtype: tuple
    :param chosen_words: dictionary, contains words which the user wants to
    learn
    :return: tuple, learning_state, learning_stats: information about learning
    """

    # TODO dictionary learning_state will contain all variables
    #      including variables from learning_stats

    # New dictionary learning_state is created
    learning_state = {}

    for key, value in chosen_words.items():

        # Dictionary learning_state is filled with keys from chosen_words
        # and each of those keys contains 'value', 'learned' and 'all_mistakes'
        # 'value' is the value of each key from chosen_words
        learning_state[key] = {'value': value,
                               # At the beginning are all words from
                               # chosen_words unlearned (False)
                               # When they are learned, they change to True
                               'learned': False,
                               # Key all_mistakes contains count of all
                               # mistakes during learning
                               # It is important for calculation how many
                               # times is the word used in next round
                               'all_mistakes': 0}

    # Dictionary learning_stats contains another variables which are not
    # related to single words:
        # ordered_words (at the beginning of each round words which should
        # be learned are prepared)
        # round_mistakes (count of mistakes during round, at the beginning of
        # each round is set to 0)
        # successful, unsuccessful: count of (un)successful attempts during
        # learning)
    learning_stats = {'ordered_words': list(chosen_words.keys()),
                      'round_mistakes': 0,
                      'successful': 0,
                      'unsuccessful': 0}

    return learning_state, learning_stats


def guess_word(guess: str, guessed: str, learning_state: dict, learning_stats: dict) -> tuple:
    """
    Checks whether word is answered correctly and returns message about the
    verdict.
    :rtype: tuple
    :param guess: str, first item from learning_stats['ordered_words']
    :param guessed: str, value of guess from learning_state[guess]['value']
    :param learning_state: dict, information about learning - each word
    :param learning_stats: dict, information about learning - together
    :return: tuple, result: message about guessing;
    learning_state, learning_stats: information about learning
    """

    # White characters from the beginning and from the end
    # of guessed word are stripped
    guessed.strip()

    # If guessed word is equal to value of ordered word,
    # this attempt is successful
    # The result is prepared and 1 point is added to successful counter
    if guessed == learning_state[guess]['value']:
        result = f'Right! Translation of "{guess}" is "{guessed}".'
        learning_stats['successful'] += 1

    # If guessed is not equal to value of ordered word,
    # this attempt is unsuccessful
    # The result with correct translation is prepared
    # and 1 point is added to following three counters:
        # all_mistakes (number of all mistakes during learning - each word)
        # round_mistakes(number of mistakes during round - together}
        # unsuccessful (number of unsuccessful attempts)
    else:
        result = f'Wrong! Correct translation of "{guess}" is ' \
                 f'"{learning_state[guess]["value"]}".'
        learning_state[guess]['all_mistakes'] += 1
        learning_stats['round_mistakes'] += 1
        learning_stats['unsuccessful'] += 1

    return result, learning_state, learning_stats


def all_learned(learning_stats: dict) -> tuple:
    """
    Checks whether all words have been learned.
    The function returns message about the success and about number
    of (un)successful attempts. Otherwise the function returns None.
    :rtype: tuple
    :param learning_stats: dict, information about learning - together
    :return: tuple, message: str, information whether all words have been
    learned; successful, unsuccessful: information about number of
    (un)successful attempts of guessing
    """

    # When there are no mistakes in current round, learning is done,
    # the function returns message about the success and about count
    # of (un)successful attempts.
    if learning_stats['round_mistakes'] == 0:
        message = f"Good job! You already know all words!"\

        successful = learning_stats['successful']
        unsuccessful = learning_stats['unsuccessful']

    # When there are some round_mistakes, the function ends
    # and returns None
    else:
        message = None
        successful = None
        unsuccessful = None

    return message, successful, unsuccessful


def prepare_next_round(learning_state: dict, learning_stats: dict) -> tuple:
    """
    Prepares next learning round.
    According to count of mistakes during learning the words are
    more or less often ordered.
    :rtype: tuple
    :param learning_state: dict, information about learning - each word
    :param learning_stats: dict, information about learning - together
    :return: tuple, learning_state, learning_stats: information about learning
    """

    # Variable round_mistakes is set to 0
    learning_stats['round_mistakes'] = 0

    # Variable ordered_words is loaded again with words, which are not learned.
    # According to count of mistakes during learning the words are
    # more or less often ordered.
    for key in learning_state:
        if learning_state[key]['learned'] is False:
            count = learning_state[key]['all_mistakes']
            learning_stats['ordered_words'].extend([key] * count)

    # The list with ordered_words is shuffled
    shuffle(learning_stats['ordered_words'])

    return learning_state, learning_stats
