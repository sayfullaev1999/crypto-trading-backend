class AuthenticationError(Exception):
    """Base authentication exception."""


class InvalidCredentialsError(AuthenticationError):
    """Invalid email or password."""


class InvalidTokenError(AuthenticationError):
    """Invalid token."""
