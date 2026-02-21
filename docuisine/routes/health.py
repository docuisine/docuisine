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
    FRONTEND_REPO = "docuisine/docuisine-react"
    BACKEND_REPO = "docuisine/docuisine"

    return health_schemas.Configuration(
        frontendLatestVersion=service.getLatestVersion(FRONTEND_REPO),
        frontendLatestCommitHash=service.getLatestCommitHash(FRONTEND_REPO),
        backendVersion=env.VERSION,
        backendLatestVersion=service.getLatestVersion(BACKEND_REPO),
        backendCommitHash=env.COMMIT_HASH,
        backendLatestCommitHash=service.getLatestCommitHash(BACKEND_REPO),
        backendDeployment=env.DEPLOYMENT,
        defaultSecretsUsed=service.get_default_secrets_used(),
        databaseURL=env.DATABASE_URL,
        databaseType=service.getDatabaseType(),
    )


@router.get("/logs", response_model=list[str])
async def get_logs(
    user: AuthenticatedUser,
    level: str = "info",
):
    """
    Retrieve application logs.

    Access Level: Admin
    """
    validate_role(user.role, "a")
    service = HealthService()
    logs = service.get_logs(level=level)
    return logs
