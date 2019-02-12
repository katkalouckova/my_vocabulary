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





