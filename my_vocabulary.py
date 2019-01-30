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

        # In such case new empty dictionary chosen_words is created
        except FileNotFoundError:
            self.chosen_words = {}

        self.source = source

    def add_word(self, required_word):
        """
        Adds required_word into self.chosen words.
        When required_word is already in self.chosen_words or when
        required_word is not in self.source the function
        returns an informative message.
        :rtype: str
        :param required_word: str, word which the user wants to add into
        self.chosen_words
        :return: message about (un)successful addition
        """

        # It is searched by keys
        # The word is already in self.chosen_words
        if required_word in self.chosen_words:
            return ("This word has been already added. "
                    "Try adding another word.")

        # Successfully addition
        elif self.source.search(required_word):
            self.chosen_words[required_word] = self.source.value(required_word)
            self.save()
            return "The word has been successfully added."

        else:
            # The word is not in self.source
            return ("This word is not in used dictionary. "
                    "Try adding another word.")

    def delete_word(self, required_word):
        """
        Deletes required_word from self.chosen_words.
        :rtype: str
        :param required_word: word which the user wants to delete from
        self.chosen_words
        :return: message about (un)successful deletion
        """

        # It is searched by keys
        # Required_word is deleted
        if required_word in self.chosen_words:
            del self.chosen_words[required_word]
            self.save()
            return "This word has been successfully deleted."

        else:
            # Required_word is not in selected dictionary
            return ("This word is not in MY VOCABULARY. "
                    "Try deleting another word.")

    def delete_selected(self, required_words):
        """
        Deletes all required_words from self.chosen_words.
        :param required_words: words which the user wants to delete
        from self.chosen_words
        :return: message about (un)successful deletion
        """

        # Counter of deleted words
        deleted = 0

        # It is searched by keys
        # All required_words are deleted
        # 1 point is added to the counter after each deletion
        for required_word in required_words:
            if required_word in self.chosen_words:
                del self.chosen_words[required_word]
                deleted += 1

        self.save()

        # One word deleted
        if deleted == 1:
            return "Selected word has been successfully deleted."

        # More words deleted
        elif deleted > 1:
            return f'{deleted} words have been successfully deleted.'

    def save(self):
        """
        Saves self.chosen_words to the disk.
        """

        with open('save_mv.txt', mode='w', encoding='utf-8') as saved:
            saved_vocabulary = json.dumps(self.chosen_words)
            print(saved_vocabulary, file=saved)


class AllWords:

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
        if required in self.content:
            return True

    def value(self, key):
        return self.content[key]
