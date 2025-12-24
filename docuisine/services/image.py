from functools import cached_property
from hashlib import md5
from io import BytesIO

import boto3
from botocore import client
from botocore.exceptions import ClientError
from PIL import Image, ImageFile

from docuisine.schemas.enums import ImageFormat
from docuisine.schemas.image import S3Config
from docuisine.utils.errors import UnsupportedImageFormatError


class ImageService:
    BUCKET_NAME = "docuisine-images"

    def __init__(
        self,
        s3_config: S3Config,
    ):
        self.s3: client.BaseClient = boto3.client(
            "s3",
            endpoint_url=s3_config.endpoint_url,
            aws_access_key_id=s3_config.access_key,
            aws_secret_access_key=s3_config.secret_key,
        )

        try:
            self.s3.head_bucket(Bucket=self.BUCKET_NAME)
        except ClientError:
            self.s3.create_bucket(Bucket=self.BUCKET_NAME)

    def upload_image(self, image: bytes) -> str:
        """
        Upload an image to the S3 bucket.

        Parameters
        ----------
        image_bytes : bytes
            The image data in bytes.

        Returns
        -------
        str
            The name of the uploaded image.
        """
        buffer = BytesIO(image)
        buffer.seek(0)

        format = self._determine_format(buffer)
        self._validate_format(format)
        image_name = self._build_image_name(image, format)
        buffer.seek(0)

        self.s3.upload_fileobj(
            Bucket=self.BUCKET_NAME,
            Key=image_name,
            Fileobj=buffer,
            ExtraArgs={"ContentType": f"image/{format}"},
        )
        return image_name

    @staticmethod
    def _build_image_name(image_bytes: bytes, format: str) -> str:
        """
        Build a unique image name based on the MD5 hash of the image bytes.
        Parameters
        ----------
        image_bytes : bytes
            The image data in bytes.
        format : str
            The image format.

        Returns
        -------
        str
            The generated image name.
        """
        image_hash = md5(image_bytes).hexdigest()
        return f"{image_hash}.{format}"

    @staticmethod
    def _determine_format(image: BytesIO) -> str:
        """
        Determine the format of the given image bytes.


        Parameters
        ----------
        image : BytesIO
            The image data in bytes.

        Returns
        -------
        str
            The format of the image.
        """
        ## Open regardless of truncated images
        ImageFile.LOAD_TRUNCATED_IMAGES = True  # type: ignore
        with Image.open(image) as img:
            return img.format.lower()

    def _validate_format(self, format: str) -> None:
        """
        Validate if the given image format is supported.

        Parameters
        ----------
        format : str
            The image format to validate.

        Raises
        ------
        UnsupportedImageFormatError
            If the image format is not supported.
        """
        if format.lower() not in self._supported_formats:
            raise UnsupportedImageFormatError(format=format.lower())

    @cached_property
    def _supported_formats(self) -> set[str]:
        """
        Return the set of supported image formats.
        """
        return {fmt.value.lower() for fmt in ImageFormat}
