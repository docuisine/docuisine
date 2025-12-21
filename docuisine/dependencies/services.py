from typing import Annotated

from fastapi import Depends

from docuisine.services import UserService

from .db import DB_Session


def get_user_service(
    db_session: DB_Session,
) -> UserService:
    return UserService(db_session)


User_Service = Annotated[UserService, Depends(get_user_service)]
