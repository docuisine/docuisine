from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from docuisine.schemas import Role

from .base import Base


class User(Base):
    """
    User model representing a user in the system.

    Attributes:
        id (int): Primary key identifier for the user.
        email (str): Unique email address of the user.
        password (str): Hashed password of the user.
        role (str): Role of the user in the system (e.g., admin, user).
        created_at (datetime): Timestamp when the user was created.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default=Role.USER.value)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
