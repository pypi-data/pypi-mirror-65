from functools import wraps
from logging import getLogger
from dataclasses import dataclass, field

import requests


logger = getLogger(__name__)


@dataclass
class TokenClient:
    """Client base class which handles authentication via the Tokens API.

    This is mostly just a wrapper around the requests library, which updates
    request headers with a JWT from the Tokens API for authentication.
    """

    tokens_api_endpoint: str = field(repr=False, default='')
    tokens_username: str = field(repr=False, default='')
    tokens_password: str = field(repr=False, default='')
    jwt_disabled: bool = field(repr=False, default=False)
    token: str = ''

    def __post_init__(self):
        """Set tokens Authorization header and add it to client requests."""
        self.header = {}

        if not self.jwt_disabled:
            self.set_auth_header()

        self.get = self.authenticated_request(requests.get)
        self.post = self.authenticated_request(requests.post)

        self._cache = {}  # prevent repeating queries

    def get_token(self):
        """Fetch token from Tokens API."""

        if self.jwt_disabled:
            return ''

        credentials = {
            'email': self.tokens_username,
            'password': self.tokens_password
        }
        response = requests.post(self.tokens_api_endpoint, json=credentials)

        if response.status_code != 200:
            raise ValueError(response.content.decode('utf-8'))

        return response.json()['data'][0]['token']

    def set_token(self):
        token_requirements = (
            self.tokens_api_endpoint,
            self.tokens_username,
            self.tokens_password,
        )

        if not all(token_requirements):
            raise TypeError(
                "'jwt_disabled' has been set to 'False'. "
                "Please specify tokens_api endpoint and login credentials."
            )

        self.token = self.get_token()

    def set_auth_header(self, token_has_expired=False):
        """Sets Authorization header for the client using the Bearer schema.

        Args:
            token_has_expired (bool): True if token has expired.
        """
        if not self.token or token_has_expired:
            self.set_token()

        self.header.update(Authorization=f'Bearer {self.token}')

    def authenticated_request(self, func):
        """Decorator to add token authentication to requests."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs.setdefault('headers', {}).update(self.header)
            response = func(*args, **kwargs)

            if response.status_code == 401:  # Assume token has expired
                self.set_auth_header(token_has_expired=True)
                response = func(*args, **kwargs)

            return response

        return wrapper

    def __str__(self):
        return self.__class__.__name__
