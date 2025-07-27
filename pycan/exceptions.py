"""Exeption class"""
from typing import Optional

class ErrorHanler(Exception):
    def __init__(self, message: str = "",
                 error_code: Optional[int] = None) -> None:
        self.error_code = error_code
        super().__init__(message if error_code is None else f"{message} [Error Code] {error_code}")

class NotImplementedFunc(ErrorHanler):
    """Indicate an error while accessing not Implement function"""
    
class ValueErrorHandler(ErrorHanler):
    """Indicate an error while accessing the particular value"""

class InitializationError(ErrorHanler):
    """Indicate an Error while Initialization"""
