import pytest
from learning_process import LearningProcess
from learning_state import LearningState
from my_vocabulary import MyVocabulary, AllWords


@pytest.mark.parametrize(["guess", "guessed"],
                         [("koupit", "buy"),
                          ("být", "be"),
                          ("postavit", "build")],
                         )
def test_guess_word_successfully(guess, guessed):
    my_vocabulary = MyVocabulary(AllWords())
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}

    learning_process = LearningProcess(LearningState(my_vocabulary))

    assert learning_process.check_guessing(guess, guessed)


@pytest.mark.parametrize(["guess", "guessed"],
                         [("koupit", "koupit"),
                          ("být", "bee"),
                          ("postavit", "buil")],
                         )
def test_guess_word_unsuccessfully(guess, guessed):
    my_vocabulary = MyVocabulary(AllWords())
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}

    learning_process = LearningProcess(LearningState(my_vocabulary)
                                       )
    assert not learning_process.check_guessing(guess, guessed)


def test_guessed():
    learning_state = LearningState(MyVocabulary(AllWords()))
    s = learning_state.successful

    learning_process = LearningProcess(learning_state)
    learning_process.guessed()

    assert learning_state.successful == s + 1


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_not_guessed(key):
    my_vocabulary = MyVocabulary(AllWords())
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}

    learning_state = LearningState(my_vocabulary)
    a = learning_state.words[key]['all_mistakes']
    u = learning_state.unsuccessful
    r = learning_state.round_mistakes

    learning_process = LearningProcess(learning_state)
    learning_process.not_guessed(key)

    assert learning_state.words[key]['all_mistakes'] == a + 1
    assert learning_state.round_mistakes == r + 1
    assert learning_state.unsuccessful == u + 1


def test_check_all_learned_true():
    learning_state = LearningState(MyVocabulary(AllWords))
    learning_state.round_mistakes = 0

    learning_process = LearningProcess(learning_state)

    assert learning_process.check_all_learned() is True


@pytest.mark.parametrize("number", [1, 10, 30])
def test_check_all_learned_false(number):
    learning_state = LearningState(MyVocabulary(AllWords))
    learning_state.round_mistakes = number

    learning_process = LearningProcess(learning_state)

    assert learning_process.check_all_learned() is False


def test_get_result():
    learning_state = LearningState(MyVocabulary(AllWords()))
    learning_state.successful = 5
    learning_state.unsuccessful = 1

    learning_process = LearningProcess(learning_state)

    assert learning_process.get_result() == (5, 1)


def test_prepare_next_round():
    learning_state = LearningState(MyVocabulary(AllWords()))
    learning_state.round_mistakes = 2
    learning_state.words = {"koupit": {"learned": False,
                                       "all_mistakes": 2},
                            "být": {"learned": True,
                                    "all_mistakes": 1},
                            "postavit": {"learned": False,
                                         "all_mistakes": 2}}

    learning_process = LearningProcess(learning_state)
    learning_process.prepare_next_round()

    assert learning_state.round_mistakes == 0
    assert sorted(learning_state.ordered_words) == ["koupit", "koupit",
                                                    "postavit", "postavit"]
