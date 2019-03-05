class BaseController:
    """
    Class for common methods of all controllers.
    """

    def __init__(self, request):
        self.request = request

    def check_request(self, arg):
        """
        Checks whether arg is in requests.args.
        :param arg: name of the request
        :return: bool
        """

        return arg in self.request.args

    def check_input(self, arg):
        """
        When there is something in input, the input is transformed to string,
        stripped and returned,
        otherwise is returned None.
        :param arg: name of the request
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
