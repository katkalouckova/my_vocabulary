import pytest
from learning import LearningState
from my_vocabulary import MyVocabulary, AllWords


def __prepare():
    return LearningState(MyVocabulary(AllWords()))


@pytest.mark.parametrize("round_mistakes", [0, 3, 100])
def test_round_mistakes_clear(round_mistakes):
    learning_state = __prepare()
    learning_state.round_mistakes_clear()
    assert learning_state.round_mistakes == 0


@pytest.mark.parametrize("successful", [0, 3, 100])
def test_increment_successful(successful):
    learning_state = __prepare()
    n = learning_state.successful
    learning_state.increment_successful()
    assert learning_state.successful == n + 1


@pytest.mark.parametrize(["key", "value"],
                         [("koupit", "buy"),
                          ("být", "be"),
                          ("postavit", "build")],
                         )
def test_value(key, value):
    my_vocabulary = MyVocabulary(AllWords)
    my_vocabulary.chosen_words = {"koupit": "buy", "být": "be",
                                  "postavit": "build"}
    learning_state = LearningState(my_vocabulary)
    assert learning_state.value(key) == value


def test_unlearned():
    learning_state = __prepare()

    util = {"koupit": False, "být": True, "postavit": False}

    # When there is something in learning_state.words, clear it
    learning_state.words = {}
    unlearned = []

    for word, learned in util.items():
        learning_state.words[word] = {'learned': learned}
        if learned is False:
            unlearned.append(word)

    assert learning_state.unlearned() == unlearned


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_set_learned(key):
    learning_state = __prepare()

    util = {"koupit": False, "být": True, "postavit": False}

    # When there is something in learning_state.words, clear it
    learning_state.words = {}

    for word, learned in util.items():
        learning_state.words[word] = {'learned': learned}

    learning_state.set_learned(key)

    assert learning_state.words[key]['learned'] is True


@pytest.mark.parametrize("key", ["koupit", "být", "postavit"])
def test_all_mistakes(key):
    learning_state = __prepare()

    util = {"koupit": 2, "být": 9, "postavit": 0}

    # When there is something in learning_state.words, clear it
    learning_state.words = {}

    for word, all_mistakes in util.items():
        learning_state.words[word] = {'all_mistakes': all_mistakes}

    assert learning_state.all_mistakes(key) == util[key]


def test_delete_first_ordered():
    learning_state = __prepare()

    learning_state.ordered_words = ["koupit", "postavit"]
    learning_state.delete_first_ordered_word()

    assert learning_state.ordered_words == ["postavit"]


def test_clear():
    my_vocabulary = MyVocabulary(AllWords)
    my_vocabulary.chosen_words = {"koupit": "buy"}
    learning_state = LearningState(my_vocabulary)
    learning_state.words['koupit']['learned'] = True

    learning_state.reset()

    assert learning_state.words["koupit"]['learned'] is False
