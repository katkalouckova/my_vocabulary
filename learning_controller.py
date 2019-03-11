import os

from flask import render_template
from my_vocabulary import MyVocabulary
from learning import LearningState, LearningProcess
from base_controller import BaseController


class LearningController(BaseController):
    """
    A class for managing learning process with requests from the user
    and preparing html render_template.
    Instance attributes:
        * self.message: message about learning
        * self.offered_word: word fo guessing
        * self.answered_word: word which the user enters
        * self.is_done: information about the end of learning
        * self.result: message about result of learning
        * self.successful: number of successful guessing during learning
        * self.unsuccessful: number of unsuccessful guessing during learning
        * self.my_vocabulary: instance of the class MyVocabulary
        * self.learning_state: instance of the class LearningState
        * self.learning_process: instance of the class LearningProcess
        * self.request: data entered by the user on html page
    """

    def __init__(self, request):
        super().__init__(request)
        self.message = None
        self.offered_word = None
        self.answered_word = None
        self.is_done = False
        self.result = None
        self.successful = 0
        self.unsuccessful = 0

        self.my_vocabulary = MyVocabulary()
        self.learning_state = LearningState(self.my_vocabulary)
        self.learning_process = LearningProcess(self.learning_state)

    def prepare_the_end(self):
        """
        Executes all necessary statements after learning (prepares the result,
        is_done changes to True, clears learning_state).
        :return: None
        """

        self.successful, self.unsuccessful = self.learning_process.get_result()
        self.message = "Good job! You already know all words!"
        # Information about the end of learning (changes the html page)
        self.is_done = True
        # Reset learning_state for another learning
        os.remove('save_learning_state.txt')
        self.learning_state.reset_learning_state()

    def process_continue(self):
        """
        Processes what should happen when the user presses "continue" (deletes
        first ordered word, if it is needed, prepares the end of learning or
        prepares next round).
        :return: None
        """

        # Ordered word from previous guessing is deleted
        self.learning_state.delete_first_ordered_word()

        # No ordered_words anymore
        if not self.learning_state.ordered_words:
            if self.learning_process.is_all_learned():
                # The end of learning
                self.prepare_the_end()

            else:
                # The end of round
                self.learning_process.prepare_next_round()

    def set_next_word(self):
        """
        Sets new self.ordered_word for next round.
        :return: None
        """

        self.offered_word = self.learning_process.get_offered_word()

    def set_answered_word(self):
        """
        Sets self.answered_word without white chars at the beginning
        and at the end of string from self.request.args.
        :return: None
        """

        self.answered_word = self.request.args['answered_word']
        self.answered_word.strip()

    def process_enter_answered(self):
        """
        Processes what should happen when the user presses "enter-answered"
        (sets self.answered_word, checks guessing, increments counters and
        prepares message about success/fail).
        :return: None
        """

        self.set_answered_word()

        # Word is guessed
        if self.learning_process.check_guessing(self.offered_word,
                                                self.answered_word):
            self.learning_process.increment_success_counter()
            self.result = f'Right! Translation of "{self.offered_word}" is ' \
                          f'"{self.answered_word}".'
        else:
            # Not guessed
            self.learning_process.increment_fail_counters(self.offered_word)
            value = self.learning_state.words[self.offered_word]["value"]
            self.result = f'Wrong! Correct translation of ' \
                f'"{self.offered_word}" is "{value}".'

    def handle_learning_controller(self):
        """
        Handles process of learning.
        :return: None
        """

        # No chosen_words
        if not self.my_vocabulary.chosen_words:
            self.message = 'MY VOCABULARY is empty. Add some words.'
            return

        # User wants to continue with learning
        if self.is_in_args('continue'):
            self.process_continue()

        # New word
        if not self.is_done:
            self.set_next_word()

        # The user wants to confirm his/her answer
        if self.is_in_args('enter-answered'):
            self.process_enter_answered()

    def prepare_render_template(self):
        """
        Returns render_template for learning page.
        :return: str
        """

        return render_template(
            'learning.html',
            message=self.message,
            is_done=self.is_done,
            result=self.result,
            offered_word=self.offered_word,
            successful=self.successful,
            unsuccessful=self.unsuccessful
            )
