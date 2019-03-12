import json
from database import Database


class Dictionary:
    """
    A class for storage and manipulation of used dictionary.
    Instance attributes:
        * self.content: words from used dictionary
    """

    def __init__(self):
        self.db = Database()

    def word_is_in_dictionary(self, required_word):
        """
        Checks if the word is in used dictionary.
        :param required_word: str, answered word
        :return: bool
        """

        cursor = self.db.get_cursor()

        is_in_dictionary = "SELECT COUNT(*) FROM czech WHERE term = %s"
        cursor.execute(is_in_dictionary, (required_word,))
        count = cursor.fetchone()[0]

        cursor.close()

        return count > 0

    def get_value(self, key):
        """
        Returns value of key from the dictionary (english equivalent).
        :param key: str, key from the dictionary (czech equivalent)
        :return: list
        """

        cursor = self.db.get_cursor_tuples()

        get_value = "SELECT EN.term " \
                    "FROM my_vocabulary.english EN " \
                    "INNER JOIN my_vocabulary.translation T " \
                    "ON EN.id = T.english_id " \
                    "INNER JOIN my_vocabulary.czech CZ " \
                    "ON T.czech_id = CZ.id " \
                    "WHERE CZ.term = %s"
        cursor.execute(get_value, (key,))
        values = [row.term for row in cursor.fetchall()]

        cursor.close()

        return values[0]


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
