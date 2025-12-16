from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Status(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthCheck(BaseModel):
    status: Status = Field(..., example=Status.HEALTHY)
    commit_hash: str = Field(..., example="a1b2c3d")
    version: str = Field(..., example="1.0.0")

    @field_validator("commit_hash", mode="before")
    def check_commit(cls, hash: str) -> str:
        if len(hash) != 7:
            raise ValueError("Commit hash must be exactly 7 characters long.")
        return hash

    @field_validator("version", mode="before")
    def check_version(cls, version: str) -> str:
        if version.count(".") != 2:
            raise ValueError("Version must be in the format 'X.Y.Z'.")

        if not all(part.isdigit() for part in version.split(".")):
            raise ValueError("Version parts must be numeric.")
        return version
