from random import shuffle


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
