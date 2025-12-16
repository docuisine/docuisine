from pydantic import BaseModel, Field

from .common import CommitHash, Status, Version


class HealthCheck(BaseModel):
    status: Status = Field(
        ..., examples=[Status.HEALTHY], description="The health status of the application."
    )
    commit_hash: CommitHash = Field(
        ...,
        examples=["a1b2c3d", "4e5f6g7"],
        description="The Git commit hash of the current build in the backend.",
    )
    version: Version = Field(
        ...,
        examples=["1.0.0", "2.5.3"],
        description="The version of the application in the backend.",
    )
