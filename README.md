# MY VOCABULARY

## Application for creating individualized vocabulary and learning stored words

WIP! (newest version is in branch database_storage)

It is a Flask application written in Python.

There are two possibilities what to do:
1. work with my vocabulary
2. learn words from my vocabulary


WORK WITH MY VOCABULARY

It is currently possible to work with the vocabulary as follows:
- add new words
- delete words

When there are some words in the vocabulary, they are shown 
under the input textfield.

There is a checkbox in front of every word from the vocabulary.
This checkbox can be selected and the user can delete selected word(s).
It is possible to check all the visible checkboxes(all the visible words)
and delete them all. 


LEARN WORDS FROM MY VOCABULARY

When there are some words in the vocabulary, it is possible to learn words
from the vocabulary.

Algorithm of learning module:
- in first round all words from the vocabulary are offered
- the words which are guessed are learned and they are not offered anymore
- in next rounds words which were not guessed are offered
- the number of offering each word is dependent on number of unsuccessful 
attempts during guessing
- learning is done, when there are no more unlearned words
- the user is informed about number of successful and unsuccessful attempts
during learning 


TO DO

- tests for work with database
- method get_value(key) in class Dictionary should return list of values
- saving my_vocabulary and learning_state in the database
- work with more words saved in my vocabulary (folders, more pages viewing, 
various limits)
- multiple users
- downloading of pronunciation
- material design into html and css

