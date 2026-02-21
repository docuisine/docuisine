from typing import Optional

import cachetools.func
import httpx
from loguru import logger

from docuisine.core.config import env


class HealthService:
    def __init__(self):
        pass

    @staticmethod
    @cachetools.func.ttl_cache(maxsize=10, ttl=300)
    def getLatestVersion(repo: str) -> Optional[str]:
        """
        Retrieve the latest version of a given repository.

        Parameters
        ----------
        repo : str
            The repository name in the format 'owner/repo'.

        Returns
        -------
        Optional[str]
            The latest version string of the specified repository.

        Example
        -------
        >>> HealthService.getLatestVersion("docuisine/docuisine")
        "2.5.3"
        """
        logger.debug(f"Fetching latest release version for repo={repo}")
        resp = httpx.get(f"https://api.github.com/repos/{repo}/releases/latest")
        return resp.json().get("tag_name")

    @staticmethod
    @cachetools.func.ttl_cache(maxsize=10, ttl=300)
    def getLatestCommitHash(repo: str) -> Optional[str]:
        """
        Retrieve the latest commit hash of a given repository.

        Parameters
        ----------
        repo : str
            The repository name in the format 'owner/repo'.

        Returns
        -------
        Optional[str]
            The latest commit hash string of the specified repository.

        Example
        -------
        >>> HealthService.getLatestCommitHash("docuisine/docuisine")
        "dfc8b734be62edfe78273aeb8a95b234aafdd987"
        """
        logger.debug(f"Fetching latest commit hash for repo={repo}")
        resp = httpx.get(f"https://api.github.com/repos/{repo}/commits/master")
        return resp.json().get("sha")

    @property
    def default_secrets(self):
        """
        Retrieve default secret usage status.

        Returns
        -------
        dict
            A dictionary containing default secret usage status.
        """
        return {
            "DB_USERNAME": "user",
            "DB_PASSWORD": "password",
            "S3_ACCESS_KEY": "s3user",
            "S3_SECRET_KEY": "s3password",
            "JWT_SECRET_KEY": "4e9db3a3f86d82cb45f552b9e24e7a652fbb5d3565a3f60a798f904cee6b235b",
        }

    def get_default_secrets_used(self) -> list[str]:
        """
        Check if default secrets are being used.

        Returns
        -------
        list[str]
            Returns a list of default credentials being used, or False if none are used.
        """

        used_defaults = []

        for key, default_value in self.default_secrets.items():
            current_value = getattr(env, key, None)
            if current_value == default_value:
                used_defaults.append(key)

        return used_defaults

    def getDatabaseURL(self) -> str:
        """
        Retrieve the database URL from the environment configuration.

        Returns
        -------
        str
            The database URL.
        """
        return env.DATABASE_URL

    def getDatabaseType(self) -> str:
        """
        Retrieve the type of the database from the database URL.

        Returns
        -------
        str
            The type of the database (e.g., 'postgresql', 'mysql').
        """
        if "postgresql" in env.DATABASE_URL:
            return "postgresql"
        elif "mysql" in env.DATABASE_URL:
            return "mysql"
        elif "sqlite" in env.DATABASE_URL:
            return "sqlite"
        else:
            return "unknown"

    def get_logs(self, level: str = "info") -> list[str]:
        """
        Retrieve application logs filtered by log level.

        Parameters
        ----------
        level : str, optional
            The log level to filter by (default is "info").

        Returns
        -------
        list[str]
            A list of log entries matching the specified log level.
        """
        # Placeholder implementation - replace with actual log retrieval logic
        allowed_levels = ["trace", "debug", "info", "warning", "error", "critical"]

        if level.lower() not in allowed_levels:
            logger.warning(f"Rejected log retrieval due to invalid level={level}")
            raise ValueError(
                f"Invalid log level '{level}'. Allowed levels are: {', '.join(allowed_levels)}"
            )

        with open(env.LOG_FILE_PATH, "r") as log_file:
            logs = log_file.readlines()

        filtered_logs = [log for log in logs if f"{level.upper()}" in log]
        logger.info(f"Retrieved {len(filtered_logs)} log entries for level={level.lower()}")

        return filtered_logs
