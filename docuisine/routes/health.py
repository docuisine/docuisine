from fastapi import APIRouter

from docuisine.core.config import env
from docuisine.schemas import health as health_schemas

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=health_schemas.HealthCheck)
def health_check():
    """
    Health check endpoint.

    Access Level: Public
    """
    return health_schemas.HealthCheck(
        status=health_schemas.Status.HEALTHY,
        commit_hash=env.COMMIT_HASH,
        version=env.VERSION,
    )
