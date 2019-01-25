def load_dictionary():
    """
    Loads dictionary.

    So far it is hardcoded here. In the future it will be dynamically loaded
    from some service.
    """

    # Variable all_words contains all words from selected dictionary
    # In keys are czech equivalents,
    # In values are english equivalents
    all_words = {"být": "be",
                 "bít": "beat",
                 "stát se čím": "become",
                 "začít": "begin",
                 "kousnout": "bite",
                 "foukat": "blow",
                 "rozbít": "break",
                 "přinést": "bring",
                 "postavit": "build",
                 "koupit": "buy"}

    return all_words
