from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from docuisine.core.config import Environment
from docuisine.db.models.base import Base

_engine = create_engine(Environment.DATABASE_URL, echo=True)
Base.metadata.create_all(bind=_engine)
SessionLocal = sessionmaker(bind=_engine)
