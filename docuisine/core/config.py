import os
from typing import Optional

from dotenv import load_dotenv


class Environment:
    """Environment configuration loader."""

    def __init__(self) -> None:
        load_dotenv()

    @property
    def DATABASE_URL(self) -> str:
        URL = os.getenv("DATABASE_URL")
        if URL is None:
            raise EnvironmentError("DATABASE_URL environment variable is not set.")
        return URL

    @property
    def COMMIT_HASH(self) -> Optional[str]:
        return os.getenv("COMMIT_HASH", None)

    @property
    def VERSION(self) -> Optional[str]:
        return os.getenv("VERSION", None)

    @property
    def MODE(self) -> str:
        mode = os.getenv("MODE")
        if mode is None:
            raise EnvironmentError("MODE environment variable is not set.")
        return mode


env = Environment()
