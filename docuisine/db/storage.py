import boto3
from botocore import client
from botocore.exceptions import ClientError

from docuisine.core.config import env
from docuisine.schemas.image import S3Config

s3_config = S3Config(
    endpoint_url=env.S3_ENDPOINT_URL,
    access_key=env.S3_ACCESS_KEY,
    secret_key=env.S3_SECRET_KEY,
)

s3_storage: client.BaseClient = boto3.client(
    "s3",
    endpoint_url=s3_config.endpoint_url,
    aws_access_key_id=s3_config.access_key,
    aws_secret_access_key=s3_config.secret_key,
)


# Ensure the S3 bucket exists
try:
    s3_storage.head_bucket(Bucket=s3_config.bucket_name)
except ClientError:
    s3_storage.create_bucket(Bucket=s3_config.bucket_name)
