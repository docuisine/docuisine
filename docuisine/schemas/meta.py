from enum import Enum

from pydantic import BaseModel, Field


class Status(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthCheck(BaseModel):
    status: Status = Field(..., example=Status.HEALTHY)
