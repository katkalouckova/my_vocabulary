import json


class MyVocabulary:
    """
    A class for storage and manipulation of data from MY VOCABULARY.
    Instance attributes:
        * self.chosen_words: words from MY VOCABULARY
        * self.source: used dictionary
    """

    def __init__(self, source):
        try:
            # When there is saved chosen_words, it is loaded
            with open('save_mv.txt', encoding='utf-8') as saved:
                self.chosen_words = json.loads(saved.read())

        # Dictionary created
        except FileNotFoundError:
            self.chosen_words = {}

        self.source = source

    def exists_word(self, required_word):
        """
        Checks if the word exists in used dictionary.
        :param required_word: str, guessed word
        :return: bool
        """

        return self.source.search(required_word)

    def add_word(self, required_word):
        """
        Adds required_word into self.chosen words and returns True.
        When required_word is already in self.chosen_words, returns False.
        :param required_word: str, word which the user wants to add into
        self.chosen_words
        :return: bool
        """

        # Successfully addition
        if required_word not in self.chosen_words:
            self.source.search(required_word)
            self.chosen_words[required_word] = self.source.value(required_word)
            self.save()
            return True

        else:
            return False

    def delete_word(self, required_word):
        """
        Deletes required_word from self.chosen_words and returns True.
        When required_word is not in self.chosen_words, returns False.
        :param required_word: word which the user wants to delete from
        self.chosen_words
        :return: bool
        """

        # Successfully deletion
        if required_word in self.chosen_words:
            del self.chosen_words[required_word]
            self.save()
            return True

        else:
            return False

    def delete_selected(self, required_words):
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
            if required_word in self.chosen_words:
                del self.chosen_words[required_word]
                deleted += 1

        self.save()

        return deleted

    def save(self):
        """
        Saves self.chosen_words to the disk.
        """

        with open('save_mv.txt', mode='w', encoding='utf-8') as saved:
            saved_vocabulary = json.dumps(self.chosen_words)
            print(saved_vocabulary, file=saved)


class AllWords:
    """
    A class for storage and manipulation of used dictionary.
    Instance attributes:
        * self.content: content of used dictionary
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

    def search(self, required):
        """
        Checks if required is in self.content (used dictionary).
        :param required: str, word which is searched
        :return: bool
        """

        return required in self.content

    def value(self, key):
        """
        Returns value of key from self.content (english equivalent).
        :param key: str, key from sel.content (czech equivalent)
        :return: str
        """

        return self.content[key]
