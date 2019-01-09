from random import shuffle


def learning_mode(chosen_words):
    """
    In this mode is user asked to repeat words from MY VOCABULARY.
    Words are offered depending on how many mistakes does the user
    during learning.
    """

    # The user is informed about entering into the learning mode
    print("LEARNING:\n")

    # If there are no words in chosen_words, the user is informed
    # by a message and the function ends
    if not chosen_words:
        print("MY VOCABULARY is empty. Enter some words.\n")
        return

    # in learned will be keys of words which are already learned
    unlearned = list(chosen_words.keys())
    learned = []

    # A dictionary all_mistakes is created
    # There are all keys of words from chosen_words, the value is number of
    # mistakes (how many times the user guessed not offered word)
    # Now the number of mistakes is 0
    all_mistakes = {}
    for i in unlearned:
        all_mistakes[i] = 0

    # Variable mistakes contains sum of mistakes in current round
    # (now it is -1 to run the while loop)
    mistakes = 1

    # Variable successfully contains sum of all guessed words during learning
    # Variable unsuccessfully contains sum of not guessed words
    successfully = 0
    unsuccessfully = 0

    # In first round of cycle while are offered all words twice
    ordered_words = unlearned.copy()
    shuffle(ordered_words)

    while mistakes != 0:
        # Sum of mistakes is in beginning of each round 0
        mistakes = 0

        # A dictionary round_mistakes is in beginning of each round empty
        # There are entered all keys of words in unlearned, the value is
        # a number of mistakes in each round
        # Now the number of mistakes is 0
        round_mistakes = {}
        for i in unlearned:
            round_mistakes[i] = 0

        # All words from shuffled list ordered_words are offered one by one
        # When the message "Right!" is printed
        # When the word is not guessed, the message with correct translation
        # is printed and in mistakes and all_mistakes is .
        for word in ordered_words:
            guessed = input(f"Write in english the word {word}: ").strip()

            if guessed == chosen_words[word]:
                print("Right!")
                successfully += 1
            else:
                print(f"Wrong! Correct translation is: {chosen_words[word]}.")
                mistakes += 1
                all_mistakes[word] += 1
                round_mistakes[word] += 1
                unsuccessfully += 1
            print()

        # If in current round number of mistakes is 0, learning is successfully
        # done (The user is informed by a message and function ends)
        # Information about sum of successful and unsuccessful attempts
        # are printed

        if mistakes == 0:
            print("Good job! You already know all words!")
            print(f"Successful/unsuccessful: "
                  f"{successfully}/{unsuccessfully}\n")
            return chosen_words

        # The words which are in current round without mistakes, are moved over
        # from list unlearned to list learned
        # unlearned.copy() - it is not possible to change iterated object
        for i in unlearned.copy():
            if round_mistakes[i] == 0:
                unlearned.remove(i)
                learned.append(i)

        # At the end of each round is the list ordered_words cleared
        # and words from unlearned are offered according to sum of mistakes
        # This information is in dictionary mistakes
        ordered_words.clear()

        for i in unlearned:
            ordered_words.extend(all_mistakes[i] * [i])

        # Created list ordered_words is shuffled to use it in next round
        shuffle(ordered_words)
