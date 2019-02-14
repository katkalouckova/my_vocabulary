def check_input(required_word):

    if required_word:
        required_word = str(required_word).strip()
        return required_word

    else:
        return None
