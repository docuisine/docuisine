from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel


class ErrorCode(Enum):
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    SERVER_ERROR = "server_error"


class Error(BaseModel):
    code: ErrorCode
    message: str
    details: dict = {}


class Response(BaseModel):
    data: List[Any] = []
    meta: dict = {}
    error: Optional[Error] = None
