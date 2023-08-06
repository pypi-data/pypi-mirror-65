import os
import requests
import json

from pymasmovil.errors.http_error import HTTPError
from pymasmovil.errors.authentication_error import AuthenticationError


class Client(object):

    def __init__(self, session=None):

        self.base_url = os.getenv('MM_BASEURL')

        if self.base_url is None:
            raise AuthenticationError('MM_BASEURL')

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if session:
            self.session = session
            self.headers["Authorization"] = "Bearer {}".format(self.session.session_id)

    def get(self, route, **kwargs):
        """ Sends a GET HTTP request

        Args:
            route (str): String with the route to the endpoint

        Return:
            **response**: Returns the response object
        """
        return self._send_request(
            verb="GET",
            url="{url}{route}".format(url=self.base_url, route=route),
            params=kwargs,
        ).json()

    def post(self, route, params, body):
        """ Sends a POST HTTP request

        Args:
            route (str): String with the route to the endpoint
            params (tuple): Tuple with optional parameters of the request to send
            body (dict): Dict with the body of the request to send

        Return:
            **response**: Returns the response object
        """

        return self._send_request(
            verb="POST",
            url="{url}{route}".format(url=self.base_url, route=route),
            params=params,
            payload=body,
        ).json()

    def _send_request(self, verb, url, payload=None, params={}):
        """send the API request using the *requests.request* method

        Args:
            payload (dict), params (dict)

        Returns:
            **requests.Response**: Response received after sending the request.

        .. note::
            Supported HTTP Methods: GET, POST
        """

        json_payload = None
        if payload:
            json_payload = json.dumps(payload)

        response = requests.request(verb.upper(),
                                    url,
                                    headers=self.headers,
                                    data=json_payload,
                                    params=params)

        if response.status_code != 200:
            raise HTTPError(response.status_code, response.json()[0]['errors'])

        return response
