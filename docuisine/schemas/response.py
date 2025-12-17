from typing import Any, List, Optional

from pydantic import BaseModel

from .enums import ErrorCode


class Error(BaseModel):
    code: ErrorCode
    message: str
    details: dict = {}


class Response(BaseModel):
    data: List[Any] = []
    meta: dict = {}
    error: Optional[Error] = None
