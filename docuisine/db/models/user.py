from pydantic import BaseModel, Field

from docuisine.schemas import Role


class Email:
    def __init__(self, address: str):
        if "@" not in address:
            raise ValueError("Invalid email address")
        self.address = address


class User(BaseModel):
    username: str = Field(..., example="johndoe")
    email: Email = Field(..., example=Email("johndoe@example.com"))
    role: Role = Field(..., example=Role.USER)
