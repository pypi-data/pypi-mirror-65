class AuthenticationError(Exception):
    """Raised when login credentials are missing"""

    message = """
    Autenthication failed.
    The required configuration setting {} was not found in your environment.
    To authenticate follow the instructions explained in the README:
    https://gitlab.com/coopdevs/pymasmovil#login
    """

    def __init__(self, missing_credential):
        self.message = self.message.format(missing_credential)
        super(AuthenticationError, self).__init__(self.message)
