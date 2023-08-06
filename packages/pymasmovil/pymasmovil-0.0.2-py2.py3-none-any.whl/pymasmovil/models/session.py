from pymasmovil.client import Client
from pymasmovil.errors.authentication_error import AuthenticationError
import os


class Session():

    def __init__(self, session_id):
        self.session_id = session_id

    @classmethod
    def create(cls):

        route = '/v0/login-api'

        login_params = (
            ('username', os.getenv('MM_USER')),
            ('password', os.getenv('MM_PASSWORD')),
            ('domain', 'test'),
        )

        if login_params[0][1] is None:
            raise AuthenticationError('MM_USER')
        elif login_params[1][1] is None:
            raise AuthenticationError('MM_PASSWORD')

        session = Client().post(route=route, params=login_params, body={})

        return Session(session["sessionId"])
