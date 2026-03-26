from __future__ import annotations

from fastapi import status


class AppException(Exception):
    """Base exception for all application-specific errors."""

    def __init__(
        self,
        detail: str = "An unexpected error occurred",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class NotFoundError(AppException):
    def __init__(self, detail: str = "Resource not found") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class ConflictError(AppException):
    def __init__(self, detail: str = "Resource already exists") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class ValidationError(AppException):
    def __init__(self, detail: str = "Validation error") -> None:
        super().__init__(detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
