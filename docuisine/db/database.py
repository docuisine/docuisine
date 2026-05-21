from typing import Self

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from docuisine.core.config import env
from docuisine.schemas.enums import Mode


class Transaction:
    """Used to orchestrate a 'single unit of work' between
    multiple services `docuisine.services`

    Usage
    -----
    ```
    with Transaction(session=session) as transaction:
        service1 = Service1(session=transaction.session)
        service2 = Service2(session=transaction.session)
        ...
    ```
    """

    def __init__(self, session: Session):
        self.session = session

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        try:
            if exc_type is None:
                try:
                    self.session.commit()
                except Exception:
                    self.session.rollback()
                    raise
            else:
                self.session.rollback()
        finally:
            self.session.close()

        return False


def IS_PRODUCTION() -> bool:
    """
    Check if the application is running in production mode.

    Raises
    ------
        ValueError
            If the MODE environment variable is not set to a valid value.
    """
    mode = env.MODE
    if mode not in (Mode.DEVELOPMENT, Mode.PRODUCTION, Mode.TESTING):
        raise ValueError(
            f"Invalid MODE: {mode}. Must be one of: development, production, testing."
        )
    return env.MODE == Mode.PRODUCTION


engine = create_engine(env.DATABASE_URL, echo=not IS_PRODUCTION())
SessionLocal = sessionmaker(bind=engine)
