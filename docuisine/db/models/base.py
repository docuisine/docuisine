from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Default:
    """
    Default model with common attributes.

    Attributes:
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last updated.
    """

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


class Entity(Default):
    """
    Base entity model with common attributes.
    These entities should reference real-world objects.

    Attributes:
        preview_img (Optional[str]): URL or path to the preview image.
        img (Optional[str]): URL or path to the main image.
        created_at (datetime): Timestamp when the entity was created.
    """

    preview_img: Mapped[Optional[str]]
    img: Mapped[Optional[str]]
