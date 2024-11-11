from typing import Any

from fastapi import HTTPException, status


class ServiceError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CacheError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class APICacheError(HTTPException):
    def __init__(self) -> None:
        status_code: int = status.HTTP_400_BAD_REQUEST
        detail: Any = "Cache System Error"
        super().__init__(status_code=status_code, detail=detail)


class APIGenericError(HTTPException):
    def __init__(self) -> None:
        status_code: int = status.HTTP_400_BAD_REQUEST
        detail: Any = "Error "
        super().__init__(status_code=status_code, detail=detail)


class APIServiceError(HTTPException):
    def __init__(self) -> None:
        status_code: int = status.HTTP_400_BAD_REQUEST
        detail: Any = "API Service Error"
        super().__init__(status_code=status_code, detail=detail)


class APIDatabaseError(HTTPException):
    def __init__(self) -> None:
        status_code: int = status.HTTP_400_BAD_REQUEST
        detail: Any = "Error in connection with database"
        super().__init__(status_code=status_code, detail=detail)


class UserNotFound(HTTPException):
    def __init__(self) -> None:
        status_code: int = status.HTTP_404_NOT_FOUND
        detail: Any = "User not found"
        super().__init__(status_code=status_code, detail=detail)


class StackNotFound(HTTPException):
    def __init__(self) -> None:
        status_code: int = status.HTTP_404_NOT_FOUND
        detail: Any = "Stack not found"
        super().__init__(status_code=status_code, detail=detail)
