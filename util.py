def check_input(required_word):
    """
    When there is something in input, the input is transformed to string
    and stripped and returned,
    otherwise is returned None.
    :param required_word: input
    :return: str/None
    """

    if required_word:
        required_word = str(required_word).strip()
        return required_word

    else:
        return None
