from operator import attrgetter
from typing import Optional

from cachetools import TTLCache, cachedmethod
import httpx

from docuisine.core.config import env


class HealthService:
    _frontendCache = TTLCache(maxsize=100, ttl=300)
    _backendCache = TTLCache(maxsize=100, ttl=300)

    def __init__(self):
        pass

    @cachedmethod(attrgetter("_frontendCache"))
    def getFrontendLatestVersion(self) -> Optional[str]:
        """
        Retrieve the latest version of the frontend application.

        Returns
        -------
        Optional[str]
            The latest version string of the frontend application.
        """
        resp = httpx.get("https://api.github.com/repos/docuisine/docuisine-react/releases/latest")
        return resp.json().get("tag_name")

    @cachedmethod(attrgetter("_backendCache"))
    def getBackendLatestVersion(self) -> Optional[str]:
        """
        Retrieve the latest version of the backend application.

        Returns
        -------
        Optional[str]
            The version string of the backend application.
        """
        resp = httpx.get("https://api.github.com/repos/docuisine/docuisine/releases/latest")
        return resp.json().get("tag_name")

    def getLatestCommitHash(self, repo: str) -> Optional[str]:
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
        """
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
