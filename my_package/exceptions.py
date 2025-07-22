"""Exeption class"""
from typing import Optional

class ErrorHanler(Exception):
    def __init__(self, message: str = "",
                 error_code: Optional[int] = None) -> None:
        self.error_code = error_code
        super().__init__(message if error_code is None else f"{message} [Error Code] {error_code}")

class InitializationError(ErrorHanler):
    """Indicate the Error while Initialization"""
