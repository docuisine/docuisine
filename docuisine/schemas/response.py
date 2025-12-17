from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field

from .enums import ErrorCode


class Error(BaseModel):
    code: ErrorCode = Field(..., description="A machine-readable error code")
    message: str = Field(..., description="A human-readable message describing the error",)
    details: dict = Field(default={}, description="Additional details about the error")


class Response(BaseModel):
    data: Union[List[Any], Any] = Field(
        default=[], description="The main data payload of the response"
    )
    meta: dict = Field(default={}, description="Additional metadata about the response")
    error: Optional[Error] = Field(default=None, description="Error details if any error occurred")
