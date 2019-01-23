from random import shuffle


def prepare_learning(chosen_words):
    """
    Following variables are created from chosen_words dictionary:
    * unlearned - list, words which I haven't learned yet
    * learned - list, words which I have already learned
    * all_mistakes - dictionary, keys are keys from chosen_words,
      values are count of mistakes (how many times the user didn't guess
      this word)
    * successfully - int, count of all guessed words during learning
    * unsuccessfully - int, count of not guessed words
    """

    # If there are no words in chosen_words, the user is informed
    # by a message and the function ends
    if not chosen_words:
        return "MY VOCABULARY is empty. Enter some words."

    # in unlearned will be keys of words which are already learned
    unlearned = list(chosen_words.keys())
    learned = []

    # A dictionary all_mistakes is created
    # There are all keys of words from chosen_words, the value is count of
    # mistakes (how many times the user guessed not this word)
    # Now the number of mistakes is 0
    all_mistakes = {}
    for i in unlearned:
        all_mistakes[i] = 0

    # Variable successfully contains count of all guessed words during learning
    # Variable unsuccessfully contains count of not guessed words
    successfully = 0
    unsuccessfully = 0

    # All words are offered in first round
    ordered_words = unlearned.copy()
    shuffle(ordered_words)

    # Sum of mistakes is in beginning of each round 0
    mistakes = 0

    # A dictionary round_mistakes is in beginning of each round empty
    # There are entered all keys of words in unlearned, the value is
    # a number of mistakes in each round
    # Now the number of mistakes is 0
    round_mistakes = {}
    for i in unlearned:
        round_mistakes[i] = 0

    return chosen_words, unlearned, learned, all_mistakes, successfully, \
           unsuccessfully, ordered_words, mistakes, round_mistakes


def guess_word(guessed, chosen_words, all_mistakes, mistakes,
                round_mistakes, successfully, unsuccessfully):
    """
    Guessed_word is compared with value of offered key.
    According to result of comparison is returned a message and proper
    variables are changed.
    """

    guessed.strip()

    if guessed == chosen_words[guessed]:
        result = "Right!"
        successfully += 1

    else:
        result = f"Wrong! Correct translation is: {chosen_words[guessed]}."
        mistakes += 1
        all_mistakes[guessed] += 1
        round_mistakes[guessed] += 1
        unsuccessfully += 1

    return guessed, chosen_words, all_mistakes, mistakes, round_mistakes, \
           successfully, unsuccessfully, result


def evaluate_round(mistakes, round_mistakes, successfully, unsuccessfully,
                   learned, unlearned):

    # If in current round number of mistakes is 0, learning is successfully
    # done (The user is informed by a message and function ends)
    # Information about count of successful and unsuccessful attempts
    # is printed

    if mistakes == 0:
        congratulation = "Good job! You already know all words!"
        summary = f"Successful/unsuccessful: {successfully}/{unsuccessfully}"
        return congratulation, summary

    # The words which are in current round without mistakes, are moved over
    # from list unlearned to list learned
    # unlearned.copy() - it is not possible to change iterated object
    for i in unlearned.copy():
        if round_mistakes[i] == 0:
            unlearned.remove(i)
            learned.append(i)

    return mistakes, round_mistakes, successfully, unsuccessfully, learned, \
           unlearned


def prepare_next_round(unlearned, all_mistakes):

    # At the beginning of each round is the list ordered_words cleared
    # and words from unlearned are offered according to count of mistakes
    # This information is in dictionary all_mistakes
    ordered_words = []

    for i in unlearned:
        ordered_words.extend(all_mistakes[i] * [i])

    # Created list ordered_words is shuffled to use it in next round
    shuffle(ordered_words)

    return unlearned, all_mistakes, ordered_words