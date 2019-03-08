from flask import render_template

from my_vocabulary import MyVocabulary
from base_controller import BaseController


class AdminController(BaseController):
    """
    Class for administration of MY VOCABULARY (entering or deleting words).
    After each statement my vocabulary is saved.
    Instance attributes:
        * self.my_vocabulary: instance of the class MyVocabulary
        * self.message: message above input type text
        * self.message_mv: message above table of MY VOCABULARY
    """

    def __init__(self, request):
        super().__init__(request)
        self.my_vocabulary = MyVocabulary()
        self.message = None
        self.message_mv = None

    def process_add(self):
        """
        Processes what should happen when the user presses "add"
        (successful deletion and various situations of unsuccessful
        deletion).
        :return: None
        """

        required_word = self.get_required_word('word')

        # Nothing was entered
        if not required_word:
            self.message = "Enter some word."

        # Not in used dictionary
        elif not self.my_vocabulary.word_is_in_dictionary(required_word):
            self.message = "This word is not in used dictionary. " \
                           "Try adding another word."

        # Already in my vocabulary
        elif self.my_vocabulary.word_is_in_mv(required_word):
            self.message = "This word has been already added. " \
                           "Try adding another word."

        else:
            # Successful addition
            self.my_vocabulary.add_word(required_word)
            self.message = "The word has been successfully added."

    def process_delete_word(self):
        """
        Processes what should happen when the user presses "delete"
        (successfully deletion and various situations of unsuccessfully
        deletion).
        :return: None
        """

        required_word = self.get_required_word('word')

        # Nothing was entered
        if not required_word:
            self.message = "Enter some word."

        # Not in my_vocabulary.chosen_words
        elif not self.my_vocabulary.word_is_in_mv(required_word):
            self.message = "This word is not in MY VOCABULARY. " \
                           "Try deleting another word."

        else:
            # Successful deletion
            self.my_vocabulary.delete_word(required_word)
            self.message = "This word has been successfully deleted."

    def process_delete_words(self):
        """
        Processes what should happen when the user presses "delete_words"
        (successful deletion and various situations of unsuccessful
        deletion).
        :return: None
        """

        required_words = self.get_required_words()

        # Nothing was selected
        if not required_words:
            self.message_mv = "There are no selected words to delete."

        else:
            # Successfully deletion
            deleted = self.my_vocabulary.delete_words(required_words)
            self.message_mv = f"Number of successfully deleted words:" \
                              f" {deleted}"

    def handle_admin_controller(self):
        """
        Handles administration of MY VOCABULARY.
        :return: None
        """

        # The user pressed "Add word"
        if self.is_in_args('add'):
            self.process_add()

        # "Delete" submit button was pressed
        elif self.is_in_args('delete'):
            self.process_delete_word()

        # Some words were selected and submit button "Delete" was pressed
        elif self.is_in_args('delete_words'):
            self.process_delete_words()

        # No words in MY VOCABULARY
        if not self.message and not self.my_vocabulary.chosen_words:
            self.message = "MY VOCABULARY is empty. Enter some words."

    def prepare_render_template(self):
        """
        Returns render_template for admin_page.
        :return: str
        """

        return render_template(
            'administration.html',
            message=self.message,
            message_mv=self.message_mv,
            chosen_words=self.my_vocabulary.chosen_words
            )
