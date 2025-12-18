from pydantic import BaseModel


class Detail(BaseModel):
    """
    Schema for detail messages in HTTP responses.
    Often used to convey error messages or other informational text
    in the API or routes.
    """

    detail: str
