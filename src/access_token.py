"""Access token for API requests."""

from datetime import datetime


class AccessToken:

    def __init__(
        self,
        access_token: str,
        token_type: str,
        expires_in: int,
        scope: str | None = None,
        refresh_token: str | None = None,
        expires_time=None,
    ) -> None:
        """Set up class."""
        self.__access_token = access_token
        self.__token_type = token_type
        self.__expires_in = expires_in
        if expires_time is None:
            self.__exp_time = datetime.now().timestamp() + expires_in
        else:
            self.__exp_time = expires_time
        self.__scope = scope
        self.__refresh_token = refresh_token

    def get_token(self) -> str:
        """Return token."""
        if self.__access_token:
            if self.has_token_expired():
                raise ValueError("Token expired!")
            return self.__access_token
        raise ValueError("Access Token not set!")

    def get_token_type(self) -> str:
        """Return token type."""
        if self.__token_type:
            return self.__token_type
        raise ValueError("Token Type not set!")

    def get_expires_in(self) -> int:
        """Return token Exp"""
        if self.__expires_in:
            return self.__expires_in
        raise ValueError("Token Expires in, has not been set!")

    def has_token_expired(self) -> bool:
        """Check if token has expired."""
        now = datetime.now().timestamp()
        if self.__exp_time <= now:
            return True
        return False

    def get_refresh_token(self) -> str:
        """Return token."""
        if self.__refresh_token:
            return self.__refresh_token
        raise ValueError("Refresh Token not set!")

    def get_scope(self) -> str:
        """Return scope."""
        if self.__scope:
            return self.__scope
        raise ValueError("Scope not set!")

    def to_dict(self) -> dict:
        """return as a dict."""
        return {
            "access_token": self.__access_token,
            "token_type": self.__token_type,
            "expires_in": self.__expires_in,
            "expires_time": self.__exp_time,
            "scope": self.__scope,
            "refresh_token": self.__refresh_token,
        }
