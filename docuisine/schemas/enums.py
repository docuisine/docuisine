from enum import Enum


class Status(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
