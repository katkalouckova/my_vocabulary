from dictionary import load_dictionary
from data_manipulation import load_mv, save_mv
from home_controller import handle_home

# Variable all_words contains all words from selected dictionary
all_words = load_dictionary()

# MY VOCABULARY is stored in variable chosen_words
# It contains the words which I want to learn
chosen_words = load_mv()

# This function leads to first menu
handle_home(chosen_words, all_words)

# Before leaving the program is MY VOCABULARY saved
save_mv(chosen_words)

# The program ends
exit()




