from random import shuffle


class LearningState:
    """
    A class for managing the process of learning.
    Instance attributes:
        * self.chosen_words: words which I want to learn
        * self.learning_state: contains information about learning process
    """

    def __init__(self, my_vocabulary):

        self.round_mistakes = 0
        self.successful = 0
        self.unsuccessful = 0
        self.ordered_words = list(my_vocabulary.chosen_words.keys())

        self.words = {}

        for key, value in my_vocabulary.chosen_words.items():
            self.words[key] = {'value': value,
                               'learned': False,
                               'all_mistakes': 0}

        self.my_vocabulary = my_vocabulary

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

    def value(self, key):
        """
        Returns a value to a word(key).
        :return: str
        """

        return self.words[key]['value']

    def unlearned(self):
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
        :return: None
        """

        self.words[key]['learned'] = True

    def all_mistakes(self, key):
        """
        Returns number of mistakes during learning of the word.
        :return: int
        """

        return self.words[key]['all_mistakes']


class LearningProcess:
    """
    A class for managing the process of learning.
    Instance attributes:
        * self.learning_state: information about learning_process
    """

    def __init__(self, learning_state):
        self.learning_state = learning_state

    def check_guessing(self, guess, guessed):
        """
        Checks whether word is answered correctly and returns bool.
        :param guess: str, first item from self.ordered_words
        :param guessed: str, word which the user guessed
        :return: bool
        """

        return self.learning_state.value(guess) == guessed

    def guessed(self):
        """
        Increments learning_state.successful counter.
        :return: None
        """

        self.learning_state.increment_successful()

    def not_guessed(self, key):
        """
        Increments counters:
            * learning_state.words[key]['all_mistakes']
            * learning_state.unsuccessful
            * learning_state.round_mistakes
        :param key: str, key from learning_state.words
        :return: None
        """

        self.learning_state.words[key]['all_mistakes'] += 1
        self.learning_state.unsuccessful += 1
        self.learning_state.round_mistakes += 1

    def check_all_learned(self):
        """
        Checks whether all words have been learned.
        :return: bool
        """

        return self.learning_state.round_mistakes == 0

    def get_result(self):
        """
        Returns number od (un)successful attempts during guessing.
        :return: tuple
        """

        successful = self.learning_state.successful
        unsuccessful = self.learning_state.unsuccessful

        return successful, unsuccessful

    def prepare_next_round(self):
        """
        Prepares next learning round:
            * Clears counter self.learning_state.round_mistakes.
            * Clears and fills self.learning_state.ordered_words - list of
            words for next round (according to number of mistakes during
            whole learning).
        :return: None
        """

        self.learning_state.round_mistakes_clear()

        self.learning_state.ordered_words = []

        for key in self.learning_state.words:
            if self.learning_state.words[key]['learned'] is False:
                count = self.learning_state.words[key]['all_mistakes']
                self.learning_state.ordered_words.extend([key] * count)

        shuffle(self.learning_state.ordered_words)
