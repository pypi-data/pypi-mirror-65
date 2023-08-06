from pymasmovil.errors.error import Error


class HTTPError(Exception):

    def __init__(self, status_code, errors):
        self.status_code = status_code
        self.errors = []
        for error in errors:
            self.errors.append(Error(error['statusCode'], error['message'], error['fields']))
