import json


class Dictionary:
    """
    A class for storage and manipulation of used dictionary.
    Instance attributes:
        * self.content: words from used dictionary
    """

    def __init__(self):
        self.content = {"být": "be",
                        "bít": "beat",
                        "stát se čím": "become",
                        "začít": "begin",
                        "kousnout": "bite",
                        "foukat": "blow",
                        "rozbít": "break",
                        "přinést": "bring",
                        "postavit": "build",
                        "koupit": "buy"}

    def word_is_in_dictionary(self, required_word):
        """
        Checks if the word is in used dictionary.
        :param required_word: str, guessed word
        :return: bool
        """

        return required_word in self.content

    def get_value(self, key):
        """
        Returns value of key from self.content (english equivalent).
        :param key: str, key from self.content (czech equivalent)
        :return: str
        """

        return self.content[key]


class MyVocabulary(Dictionary):
    """
    A class for storage and manipulation of data from MY VOCABULARY.
    Instance attributes:
        * self.chosen_words: words from MY VOCABULARY
        * self.source: used dictionary
    """

    def __init__(self):
        try:
            # When there is saved chosen_words, it is loaded
            with open('save_my_vocabulary.txt', encoding='utf-8') as saved:
                self.chosen_words = json.loads(saved.read())

        # Dictionary created
        except FileNotFoundError:
            self.chosen_words = {}

        super().__init__()

    def word_is_in_mv(self, required_word):
        """
        Checks if the word is in self.chosen_words.
        :param required_word: str, guessed word
        :return: bool
        """

        return required_word in self.chosen_words

    def add_word(self, required_word):
        """
        Adds required_word into self.chosen words.
        :param required_word: str, word which the user wants to add into
        self.chosen_words
        :return: None
        """

        self.chosen_words[required_word] = self.get_value(required_word)
        self.save_my_vocabulary()

    def delete_word(self, required_word):
        """
        Deletes required_word from self.chosen_words.
        :param required_word: word which the user wants to delete from
        self.chosen_words
        :return: None
        """

        del self.chosen_words[required_word]
        self.save_my_vocabulary()

    def delete_words(self, required_words):
        """
        Deletes all required_words from self.chosen_words and returns number
        of deleted words.
        :param required_words: words which the user wants to delete
        from self.chosen_words
        :return: int
        """

        # Counter of deleted words
        deleted = 0

        # It is searched by keys
        for required_word in required_words:
            del self.chosen_words[required_word]
            deleted += 1

        self.save_my_vocabulary()

        return deleted

    def save_my_vocabulary(self):
        """
        Saves self.chosen_words to the disk.
        """

        with open('save_my_vocabulary.txt', mode='w', encoding='utf-8') as saved:
            saved_vocabulary = json.dumps(self.chosen_words)
            print(saved_vocabulary, file=saved)
