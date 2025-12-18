from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from docuisine.schemas import Role

from .base import Base, Entity


class User(Base, Entity):
    """
    User model representing a user in the system.

    Attributes:
        email (str): Unique email address of the user.
        password (str): Hashed password of the user.
        role (str): Role of the user in the system (e.g., admin, user).
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(String, nullable=False, default=Role.USER.value)
