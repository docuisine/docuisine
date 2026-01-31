from typing import Optional

from pydantic import BaseModel, Field

from .annotations import CommitHash, Version
from .enums import Status


class HealthCheck(BaseModel):
    status: Status = Field(
        ..., examples=[Status.HEALTHY], description="The health status of the application."
    )
    commit_hash: Optional[CommitHash] = Field(
        ...,
        examples=["a1b2c3d", "4e5f6g7"],
        description="The Git commit hash of the current build in the backend.",
    )
    version: Optional[Version] = Field(
        ...,
        examples=["1.0.0", "2.5.3"],
        description="The current version of the backend application being used.",
    )


class Configuration(BaseModel):
    frontendLatestVersion: Optional[str] = Field(
        ...,
        examples=["1.0.0", "2.5.3"],
        description="The latest version of the frontend application.",
    )
    backendVersion: Optional[str] = Field(
        ...,
        examples=["1.0.0", "2.5.3"],
        description="The current version of the backend application being used.",
    )
    backendLatestVersion: Optional[str] = Field(
        ...,
        examples=["1.0.0", "2.5.3"],
        description="The latest version of the backend application.",
    )
    defaultSecretsUsed: Optional[list[str]] = Field(
        ...,
        examples=[["DB_USERNAME", "DB_PASSWORD"], []],
        description="A list of default secrets being used in the application.",
    )
