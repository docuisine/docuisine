from fastapi import APIRouter, HTTPException, status

from docuisine.db.models import User
from docuisine.dependencies import User_Service
from docuisine.schemas import user as user_schemas
from docuisine.schemas.enums import Role
from docuisine.utils import errors

router = APIRouter(tags=["Root"])


@router.get("/", status_code=status.HTTP_200_OK)
async def read_root():
    """
    Root endpoint.

    Access Level: Public
    """
    return "Hello, from Docuisine!"


@router.get("/init/existing-root-user", status_code=status.HTTP_200_OK)
async def init(user_service: User_Service):
    """
    Check if a root user already exists.

    Access Level: Public
    """
    try:
        user = user_service.get_user(user_id=1)
        return user is not None
    except errors.UserNotFoundError:
        return False


@router.post("/init/create-first-user", status_code=status.HTTP_200_OK)
async def create_first_user(user: user_schemas.UserCreate, user_service: User_Service):
    """
    Create the first user in the system.

    This endpoint is used to create the first user with admin privileges.
    """

    try:
        user_service.get_user(user_id=1)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Root user already exists.",
        )
    except errors.UserNotFoundError:
        pass  # No root user exists, proceed to create one

    new_user: User = user_service.create_user(
        username=user.username,
        password=user.password,
        email=user.email,
        role=Role.ADMIN,
    )

    return user_schemas.UserOut.model_validate(new_user)
