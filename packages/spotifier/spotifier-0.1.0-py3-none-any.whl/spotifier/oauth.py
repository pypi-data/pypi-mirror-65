"""Spotify OAuth.

Reference:
    https://developer.spotify.com/documentation/general/guides/authorization-guide
"""

import base64
import urllib.parse
import warnings
from typing import List, Optional, Set

import requests

import spotifier.status_codes as C

try:
    from typing import TypedDict  # type: ignore
except ImportError:
    from mypy_extensions import TypedDict


class SpotifyOAuthError(Exception):
    pass


class SpotifyScopeError(Exception):
    pass


class SpotifyStateError(Exception):
    pass


class Token(TypedDict):
    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: str


class RefreshedToken(TypedDict):
    access_token: str
    token_type: str
    scope: str
    expires_in: int


class AuthorizationHeaders(TypedDict):
    authorization: str


class SpotifyAuthorizationCode:
    """Spotify Authorization Code Flow.

    Reference:
        https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow
    """

    OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
    OAUTH_TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        state: str = None,
        scopes: List[str] = None,
        show_dialog: bool = False,
    ):
        """Spotify OAuth Client for Spotify Authorization Code Flow.

        Reference:
            https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow

        Args:
            client_id (str): Client ID provided by your Spotify application
            client_secret (str): Client Secret provided by your Spotify application
            redirect_uri (str): Redirect URI you set in your Spotify Application
            state (str, optional): State to protect from CSRF. Defaults to None.
            scopes (List[str], optional): List of scope. All scopes are in 'spotifier.scopes' Defaults to None.
            show_dialog (bool, optional): Whether to force user to approve app again if already done.
                Defaults to False.
        """
        if state is None:
            warnings.warn("Argument state should be some random string to protect from CSRF.")

        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._state = state
        self._scopes = scopes
        self._show_dialog = show_dialog

        self._token: Optional[Token] = None

    @property
    def token(self) -> Optional[Token]:
        return self._token

    @token.setter
    def token(self, token: Token):
        self._token = token

    @property
    def scopes(self) -> Optional[List[str]]:
        return self._scopes

    def get_authorize_url(self) -> str:
        """Request user to approve app to access user information.

        Returns:
            str: Authorization URL
        """

        payload = {
            "client_id": self._client_id,
            "response_type": "code",
            "redirect_uri": self._redirect_uri,
        }
        if self._state is not None:
            payload["state"] = self._state
        if self._scopes is not None:
            payload["scope"] = " ".join(self._scopes)

        return f"{self.OAUTH_AUTHORIZE_URL}?{urllib.parse.urlencode(payload)}"

    def parse_response_code(self, url: str) -> str:
        """Parse response code from redirect URL.

        Args:
            url (str): Authorization URL provided by 'get_authorize_url()'

        Raises:
            SpotifyOAuthError: When authorization failed
            SpotifyStateError: When state is not correct

        Returns:
            str: Authorization code that can be exchanged for access token
        """
        q = urllib.parse.urlparse(url).query
        query_dict = urllib.parse.parse_qs(q)

        if "error" in query_dict:
            raise SpotifyOAuthError

        if self._state is not None and query_dict["state"][0] != self._state:
            raise SpotifyStateError

        return query_dict["code"][0]

    def set_token(self, code: str) -> Token:
        """Request access token and refresh token and set it.

        This method returns set token but you don't need to receive it.

        Args:
            code (str): Authorization code provided by 'parse_response_code()'

        Raises:
            SpotifyOAuthError: When request returns other than 200 (RESPONSE_OK)

        Returns:
            Token: Authorized token
        """
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self._redirect_uri,
        }

        headers = self._make_authorization_headers(client_id=self._client_id, client_secret=self._client_secret)

        r = requests.post(self.OAUTH_TOKEN_ENDPOINT, data=payload, headers=headers)

        if r.status_code != C.RESPONSE_OK:
            raise SpotifyOAuthError

        self._token = Token(**r.json())  # type: ignore

        return self._token  # type: ignore

    def refresh_token(self) -> Token:
        """Request access token refresh.

        This method returns refreshed token but you don't need to receive it.

        Raises:
            ValueError: When token has not been set yet
            SpotifyOAuthError: When request returns other than 200 (RESPONSE OK)

        Returns:
            Token: Refreshed token
        """
        if self._token is None:
            raise ValueError("Attribute non-None token required to refresh.")

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self._token["refresh_token"],
        }

        headers = self._make_authorization_headers(client_id=self._client_id, client_secret=self._client_secret)

        r = requests.post(self.OAUTH_TOKEN_ENDPOINT, data=payload, headers=headers)

        if r.status_code != C.RESPONSE_OK:
            raise SpotifyOAuthError

        refreshed_token = RefreshedToken(**r.json())  # type: ignore
        self._token.update(refreshed_token)

        return self._token

    @staticmethod
    def is_scopes_subset(having_scopes: Optional[List[str]], required_scopes: Optional[List[str]]) -> bool:
        """Check the current oauth meets required scopes.

        Args:
            having_scopes (Optional[List[str]]): Current scopes
            required_scopes (Optional[List[str]]): Required scopes

        Returns:
            bool: [description]
        """
        having_scopes_set: Set[str] = set(having_scopes) if having_scopes is not None else set()
        required_scopes_set: Set[str] = set(required_scopes) if required_scopes is not None else set()
        return having_scopes_set >= required_scopes_set

    @staticmethod
    def _make_authorization_headers(client_id: str, client_secret: str) -> AuthorizationHeaders:
        return AuthorizationHeaders(
            authorization=f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')}"
        )
