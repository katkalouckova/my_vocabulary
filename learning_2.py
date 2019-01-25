from random import shuffle


def prepare_learning(chosen_words):
    """
    From dictionary chosen_words is created dictionary learning_state.
    Each key from chosen_words is key of this dictionary and contents
    three dictionaries with:
    * value (value from chosen_words),
    * learned (True or False),
    * all_mistakes (count of all mistakes during learning - each word)
    Another dictionary learning_stats is created. It is independent
    on particular words from chosen_words. It contents keys:
    * round_mistakes (count of mistakes during round - together}
    * successful (count of successful guessing attempts)
    * unsuccessful (count of unsuccessful attempts)
    """

    # TODO dictionary learning_state will content all variables
    # including variables from learning_stats

    # New dictionary learning_state is created
    learning_state = {}

    for key, value in chosen_words.items():

        # Dictionary learning_state is filled with keys from chosen_words
        # and each of those keys contents 'value', 'learned' and 'all_mistakes'
        # 'value' is the value of each key from chosen_words
        learning_state[key] = {'value': value,
                               # At the beginning are all words from
                               # chosen_words unlearned (False)
                               # When they are learned, they change to True
                               'learned': False,
                               # Variable all_mistakes contains count of all
                               # mistakes during learning
                               # It is important for calculation how many
                               # times is the word used in next round
                               'all_mistakes': 0}

    # Dictionary learning_stats contents another variables which are not
    # related to single words:
        # ordered_words (at the beginning of each round are prepared words
        # which should be learned)
        # round_mistakes (count of mistakes during round, at the beginning of
        # each round is set to 0)
        # successful, unsuccessful: count of (un)successful attempts during
        # learning)
    learning_stats = {'ordered_words': list(chosen_words.keys()),
                      'round_mistakes': 0,
                      'successful': 0,
                      'unsuccessful': 0}

    return learning_state, learning_stats


def guess_word(guess, guessed, learning_state, learning_stats):
    """
    White characters from the beginning and from the end
    of guessed word are stripped.
    Guessed word is compared with value of offered key.
    According to result of comparison is returned a message and proper
    variables are changed.
    """

    # White characters from the beginning and from the end
    # of guessed word are stripped
    guessed.strip()

    # If guessed word is equal to value of ordered word,
    # thus attempt is successful
    # The result is prepared and to successful is added 1 point
    if guessed == learning_state[guess]['value']:
        result = f'Right! Translation of "{guess}" is "{guessed}".'
        learning_stats['successful'] += 1

    # If guessed is not equal to value of ordered word,
    # this attempt is unsuccessful
    # The result with correct translation is prepared
    # and to three variables is added 1 point:
        # all_mistakes (count of all mistakes during learning - each word)
        # round_mistakes(count of mistakes during round - together}
        # unsuccessful (count of unsuccessful attempts)
    else:
        result = f'Wrong! Correct translation of "{guess}" is ' \
                 f'"{learning_state[guess]["value"]}".'
        learning_state[guess]['all_mistakes'] += 1
        learning_stats['round_mistakes'] += 1
        learning_stats['unsuccessful'] += 1

    return result, learning_state, learning_stats


def all_learned(learning_stats):
    """
    When there are no mistakes in current round, learning is done,
    the function returns message about the success and about count
    of successful and unsuccessful attempts.
    Otherwise the function returns None.
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

    return message, successful, unsuccessful


def prepare_next_round(learning_state, learning_stats):
    """
    Variable round_mistakes is set to 0.
    Variable ordered_words is loaded again with words,
    which are not learned.
    According to count of mistakes during learning are they
    more or less often ordered.
    The list with ordered_words is shuffled.
    """

    # Variable round_mistakes is set to 0
    learning_stats['round_mistakes'] = 0

    # Variable ordered_words is loaded again with words, which are not learned.
    # According to count of mistakes during learning are they more or less
    # often ordered.
    for key in learning_state:
        if learning_state[key]['learned'] is False:
            count = learning_state[key]['all_mistakes']
            learning_stats['ordered_words'].extend([key] * count)

    # The list with ordered_words is shuffled
    shuffle(learning_stats['ordered_words'])

    return learning_state, learning_stats
