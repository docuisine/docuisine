# config.py
from functools import cached_property
import os
import subprocess


class Environment:
    """Lazy-loaded application info, cached for efficiency."""

    @cached_property
    def git_commit_hash(self) -> str | None:
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
    def version(self) -> str:
        try:
            return (
                subprocess.check_output(["uv", "version"], stderr=subprocess.DEVNULL)
                .decode()
                .strip()
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "unknown"


env = Environment()
