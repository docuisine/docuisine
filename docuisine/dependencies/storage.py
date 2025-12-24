from typing import Annotated

from botocore import client
from fastapi import Depends

from docuisine.db.storage import s3_storage


def get_s3_client() -> client.BaseClient:
    return s3_storage


S3_Client = Annotated[client.BaseClient, Depends(get_s3_client)]
