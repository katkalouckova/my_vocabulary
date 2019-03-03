from random import shuffle


class LearningState:
    """
    A class for storage and work with information about the learning process.
    Instance attributes:
        * self.my_vocabulary: instance of class MyVocabulary
        * self.round_mistakes: number of unsuccessfully guessing during round
        * self.successful: number of successfully guessing during learning
        * self.unsuccessful: number of unsuccessfully guessing during learning
        * self.ordered_words: list of words which are offered in current round
        * self.words: dictionary, contains all words which should be learned
        and each word contains another dictionary with information about
        each word:
            - value - english equivalent
            - learned - bool (the word is learned or not)
            - total_mistakes - number of unsuccessfully guessing during learning
    """

    def __init__(self, my_vocabulary):
        self.my_vocabulary = my_vocabulary
        self.round_mistakes = 0
        self.successful = 0
        self.unsuccessful = 0
        self.ordered_words = list(self.my_vocabulary.chosen_words.keys())

        self.words = {}

        for key, value in self.my_vocabulary.chosen_words.items():
            self.words[key] = {'value': value,
                               'learned': False,
                               'total_mistakes': 0}

    def round_mistakes_clear(self):
        """
        Sets a number of round_mistakes to 0.
        :return: None
        """

        self.round_mistakes = 0

    def increment_successful(self):
        """
        Increments successful by 1.
        :return: None
        """

        self.successful += 1

    def get_value(self, key):
        """
        Returns a value of a word(key).
        :param key: str, key from learning_state.words
        :return: str
        """

        return self.words[key]['value']

    def get_unlearned(self):
        """
        Returns the list of unlearned words.
        :return: list
        """

        unlearned = []

        for i in self.words:
            if self.words[i]['learned'] is False:
                unlearned.append(i)

        return unlearned

    def set_learned(self, key):
        """
        Sets learned to True.
        :param key: str, key from learning_state.words
        :return: None
        """

        self.words[key]['learned'] = True

    def total_mistakes(self, key):
        """
        Returns number of mistakes during learning of the word.
        :param key: str, key from learning_state.words
        :return: int
        """

        return self.words[key]['total_mistakes']

    def delete_first_ordered_word(self):
        """
        Deletes first item from list self.ordered_words
        :return: None
        """

        del self.ordered_words[0]

    def reset_learning_state(self):
        """
        Clears learning_state.
        :return: None
        """

        # TODO Is there another better way to reset everything in __init__?
        self.__init__(self.my_vocabulary)


class LearningProcess:
    """
    A class for managing the process of learning.
    Instance attributes:
        * self.learning_state: information about learning_process
    """

    def __init__(self, learning_state):
        self.learning_state = learning_state

    def get_offered_word(self):
        """
        Returns first item from self.ordered_words(for guessing).
        :return: str
        """

        return self.learning_state.ordered_words[0]

    def check_guessing(self, guess, guessed):
        """
        Checks whether the word is correctly answered and returns bool.
        :param guess: str, word which should be guessed
        :param guessed: str, word which the user guessed
        :return: bool
        """

        return self.learning_state.get_value(guess) == guessed

    def increment_success_counter(self):
        """
        Increments learning_state.successful counter.
        :return: None
        """

        self.learning_state.increment_successful()

    def increment_fail_counters(self, key):
        """
        Increments counters:
            * learning_state.words[key]['total_mistakes']
            * learning_state.unsuccessful
            * learning_state.round_mistakes
        :param key: str, key from learning_state.words
        :return: None
        """

        self.learning_state.words[key]['total_mistakes'] += 1
        self.learning_state.unsuccessful += 1
        self.learning_state.round_mistakes += 1

    def is_all_learned(self):
        """
        Checks whether all words have been learned.
        :return: bool
        """

        return self.learning_state.round_mistakes == 0

    def get_result(self):
        """
        Returns number od (un)successful attempts during learning.
        :return: tuple
        """

        return self.learning_state.successful, self.learning_state.unsuccessful

    def prepare_next_round(self):
        """
        Prepares next learning round:
            * Clears counter self.learning_state.round_mistakes
            * Clears and fills self.learning_state.ordered_words - list of
            words for next round (according to number of mistakes during
            whole learning)
        :return: None
        """

        self.learning_state.round_mistakes_clear()

        self.learning_state.ordered_words = []

        for key in self.learning_state.words:
            if self.learning_state.words[key]['learned'] is False:
                
                # Dependency of frequency of offering each word
                count = self.learning_state.words[key]['total_mistakes']
                self.learning_state.ordered_words.extend([key] * count)

        shuffle(self.learning_state.ordered_words)
