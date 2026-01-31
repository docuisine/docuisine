from fastapi import APIRouter

from docuisine.core.config import env
from docuisine.dependencies import AuthenticatedUser
from docuisine.schemas import health as health_schemas
from docuisine.services import HealthService
from docuisine.utils.validation import validate_role

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=health_schemas.HealthCheck)
async def health_check():
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
async def configuration(user: AuthenticatedUser):
    """
    Retrieve application configuration details.

    Access Level: Admin
    """
    validate_role(user.role, "a")
    service = HealthService()

    return health_schemas.Configuration(
        frontendLatestVersion=service.getFrontendLatestVersion(),
        backendVersion=env.VERSION,
        backendLatestVersion=service.getBackendLatestVersion(),
        defaultSecretsUsed=service.get_default_secrets_used(),
        databaseURL=env.DATABASE_URL,
        databaseType=service.getDatabaseType(),
    )
