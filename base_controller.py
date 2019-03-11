class BaseController:
    """
    Class for common methods of all controllers.
    """

    def __init__(self, request):
        self.request = request

    def is_in_args(self, arg):
        """
        Checks whether arg is in requests.args.
        :param arg: argument name in the request
        :return: bool
        """

        return arg in self.request.args

    def get_required_word(self, arg):
        """
        Returns stripped input; when there is nothing in input, None
        is returned.
        :param arg: argument name in the request
        :return: str/None
        """

        required_word = self.request.args[arg]

        if required_word:
            required_word = str(required_word).strip()
            return required_word

        else:
            return None

    def get_required_words(self):
        """
        Returns list of required_words.
        :return: list
        """

        required_words = self.request.args.getlist('select')

        return required_words
