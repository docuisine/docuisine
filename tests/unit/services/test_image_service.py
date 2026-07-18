from hashlib import md5
from io import BytesIO
from unittest.mock import MagicMock

import pytest

from docuisine.schemas.image import ImageSet
from docuisine.services import ImageService
from docuisine.utils import errors


@pytest.fixture
def mock_s3_client(monkeypatch):
    """Fixture for mocking boto3 S3 client."""
    mock_s3 = MagicMock()
    return mock_s3


@pytest.fixture
def image_service(mock_s3_client: MagicMock, monkeypatch):
    """Fixture for ImageService with mocked S3 client and supported formats."""
    service = ImageService(s3=mock_s3_client)
    monkeypatch.setattr(service, "_supported_formats", {"png", "jpeg", "jpg", "gif"})
    return service


def test_upload_image_delegates_to_file_upload(image_service: ImageService, monkeypatch):
    """Test the byte upload path delegates to the file-based implementation."""
    expected = ImageSet(original="original.jpeg", preview="preview.jpeg")
    upload_image_file = MagicMock(return_value=expected)
    monkeypatch.setattr(image_service, "upload_image_file", upload_image_file)

    image_bytes = b"fake-image-bytes"
    image_set: ImageSet = image_service.upload_image(image_bytes)

    assert image_set == expected
    upload_image_file.assert_called_once()
    assert upload_image_file.call_args.args[0].read() == image_bytes


def test_upload_image_file(image_service: ImageService, monkeypatch, mock_s3_client: MagicMock):
    """Test uploading an image from a file-like object."""
    mock_determine_format = MagicMock(return_value="jpeg")
    monkeypatch.setattr(
        "docuisine.services.image.ImageService._determine_format", mock_determine_format
    )
    monkeypatch.setattr(
        "docuisine.services.image.ImageService._validate_format", lambda self, format: None
    )
    monkeypatch.setattr(
        "docuisine.services.image.ImageService._build_image_name_from_file",
        lambda *args: "original.jpeg",
    )
    monkeypatch.setattr(
        "docuisine.services.image.ImageService._build_image_name",
        lambda *args: "preview.jpeg",
    )
    monkeypatch.setattr(
        "docuisine.services.image.ImageService._generate_image_preview_from_file",
        lambda self, image: b"preview-image-bytes",
    )
    mock_s3_client.meta.endpoint_url = "http://mock-s3-endpoint/"
    mock_s3_client.bucket_name = "docuisine-images"

    image_file = BytesIO(b"fake-image-bytes")
    image_set: ImageSet = image_service.upload_image_file(image_file)

    assert image_set.original == "original.jpeg"
    assert image_set.preview == "preview.jpeg"
    assert mock_s3_client.upload_fileobj.call_count == 2


def test_validate_format_unsupported(image_service: ImageService, monkeypatch):
    """Test validating an unsupported image format."""

    unsupported_format = "bmp"

    with pytest.raises(errors.UnsupportedImageFormatError) as exc_info:
        image_service._validate_format(unsupported_format)

    assert str(exc_info.value) == f"Unsupported image format: {unsupported_format}"


def test_validate_format_supported(image_service):
    """Test validating a supported image format."""
    supported_format = "png"

    # This should not raise an exception
    image_service._validate_format(supported_format)


def test_build_image_name():
    """Test building image name from bytes and format."""
    image_bytes = b"test-image-bytes"
    format = "png"

    image_name = ImageService._build_image_name(image_bytes, format)

    expected_hash = md5(image_bytes).hexdigest()
    expected_image_name = f"{expected_hash}.png"

    assert image_name == expected_image_name
