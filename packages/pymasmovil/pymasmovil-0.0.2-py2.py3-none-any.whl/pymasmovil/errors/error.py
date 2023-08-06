
class Error():

    def __init__(self, status_code, message, fields):
        self.status_code = status_code
        self.message = message
        self.fields = fields
