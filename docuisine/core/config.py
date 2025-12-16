from functools import cached_property
import os
import subprocess
from typing import Union

from dotenv import load_dotenv


class Environment:
    """Lazy-loaded application info, cached for efficiency."""

    def __init__(self) -> None:
        load_dotenv()

    @property
    def DB_URL(self) -> str:
        URL = os.getenv("DATABASE_URL")
        if URL is None:
            raise EnvironmentError("DATABASE_URL environment variable is not set.")
        return URL

    @cached_property
    def git_commit_hash(self) -> Union[str, None]:
        try:
            return (
                subprocess.check_output(
                    ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
                )
                .decode()
                .strip()
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    @cached_property
    def version(self) -> Union[str, None]:
        try:
            return (
                subprocess.check_output(["uv", "version", "--short"], stderr=subprocess.DEVNULL)
                .decode()
                .strip()
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None


env = Environment()
