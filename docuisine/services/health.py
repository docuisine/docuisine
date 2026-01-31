from typing import Optional

import httpx

from docuisine.core.config import env


class HealthService:
    def __init__(self):
        pass

    def getFrontendLatestVersion(self) -> Optional[str]:
        """
        Retrieve the latest version of the frontend application.

        Returns
        -------
        Optional[str]
            The latest version string of the frontend application.
        """
        return (
            httpx.get("https://api.github.com/repos/docuisine/docuisine-react/releases/latest")
            .json()
            .get("tag_name", None)
        )

    def getBackendLatestVersion(self) -> Optional[str]:
        """
        Retrieve the latest version of the backend application.

        Returns
        -------
        Optional[str]
            The version string of the backend application.
        """
        return (
            httpx.get("https://api.github.com/repos/docuisine/docuisine/releases/latest")
            .json()
            .get("tag_name", None)
        )

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
