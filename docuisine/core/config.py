from functools import cached_property
import subprocess
from typing import Union


class Environment:
    """Lazy-loaded application info, cached for efficiency."""

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
                subprocess.check_output(["uv", "version"], stderr=subprocess.DEVNULL)
                .decode()
                .strip()
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None


env = Environment()
