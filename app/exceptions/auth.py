from __future__ import annotations

from fastapi import status

from app.exceptions.base import AppException


class AuthenticationError(AppException):
    def __init__(self, detail: str = "Could not validate credentials") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(AppException):
    def __init__(self, detail: str = "Not enough permissions") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class InvalidTokenError(AppException):
    def __init__(self, detail: str = "Invalid or malformed token") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class TokenExpiredError(AppException):
    def __init__(self, detail: str = "Token has expired") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)
