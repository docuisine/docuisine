from fastapi import APIRouter

from docuisine.core.config import env
from docuisine.schemas import health as health_schemas
from docuisine.services import HealthService

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


@router.get("/configuration", response_model=health_schemas.Configuration)
def configuration():
    """
    Retrieve application configuration details.

    Access Level: Public
    """
    service = HealthService()

    return health_schemas.Configuration(
        frontendLatestVersion=service.getFrontendLatestVersion(),
        backendVersion=env.VERSION,
        backendLatestVersion=service.getBackendLatestVersion(),
        defaultSecretsUsed=service.get_default_secrets_used(),
    )
