import os
import sys
from typing import Literal, Optional, TextIO

from dotenv import load_dotenv
from loguru import logger


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
    def DB_USERNAME(self) -> str:
        username = self.DATABASE_URL.split("@")[0].split("//")[1].split(":")[0]
        return username

    @property
    def DB_PASSWORD(self) -> str:
        password = self.DATABASE_URL.split("@")[0].split("//")[1].split(":")[1]
        return password

    @property
    def COMMIT_HASH(self) -> Optional[str]:
        if self.DEPLOYMENT == "vercel":
            return os.getenv("VERCEL_GIT_COMMIT_SHA", None)

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

    @property
    def JWT_SECRET_KEY(self) -> str:
        secret_key = os.getenv("JWT_SECRET_KEY", None)
        if secret_key is None:
            raise EnvironmentError("JWT_SECRET_KEY environment variable is not set.")
        return secret_key

    @property
    def JWT_ALGORITHM(self) -> str:
        algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        return algorithm

    @property
    def JWT_ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        expire_minutes = os.getenv(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "525600"
        )  # Default to 1 year
        return int(expire_minutes)

    @property
    def S3_ENDPOINT_URL(self) -> str:
        endpoint_url = os.getenv("S3_ENDPOINT_URL")
        if endpoint_url is None:
            raise EnvironmentError("S3_ENDPOINT_URL environment variable is not set.")
        return endpoint_url

    @property
    def S3_ACCESS_KEY(self) -> str:
        access_key = os.getenv("S3_ACCESS_KEY")
        if access_key is None:
            raise EnvironmentError("S3_ACCESS_KEY environment variable is not set.")
        return access_key

    @property
    def S3_SECRET_KEY(self) -> str:
        secret_key = os.getenv("S3_SECRET_KEY")
        if secret_key is None:
            raise EnvironmentError("S3_SECRET_KEY environment variable is not set.")
        return secret_key

    @property
    def S3_BUCKET_NAME(self) -> str:
        bucket_name = os.getenv("S3_BUCKET_NAME", "docuisine-images")
        return bucket_name

    @property
    def S3_REGION(self) -> str:
        region = os.getenv("S3_REGION", "apac")
        if region is None:
            raise EnvironmentError("S3_REGION environment variable is not set.")
        return region

    @property
    def DEPLOYMENT(self) -> Literal["docker", "vercel"]:
        """Deployment environment (e.g., docker or vercel (serverless))."""
        deployment = os.getenv("DEPLOYMENT", "docker")

        if deployment in ["docker", "vercel"]:
            return deployment  # type: ignore

        raise EnvironmentError(
            "DEPLOYMENT environment variable must be either 'docker' or 'vercel'."
        )

    @property
    def LOG_LEVEL(self) -> str:
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if log_level not in valid_levels:
            err_msg = (
                f"Invalid LOG_LEVEL '{log_level}'. Valid options are: {', '.join(valid_levels)}."
            )
            logger.critical(err_msg)
            raise EnvironmentError(err_msg)
        return log_level

    @property
    def LOG_FILE_PATH(self) -> str | TextIO:
        log_file_path = os.getenv("LOG_FILE_PATH", sys.stdout)
        return log_file_path


env = Environment()
