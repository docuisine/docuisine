from contextlib import asynccontextmanager
import json
import time

from botocore.exceptions import ClientError
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.responses import Response

from docuisine import routes
from docuisine.core.config import env
from docuisine.db.database import engine
from docuisine.db.models.base import Base
from docuisine.db.storage import s3_config, s3_storage

## Define S3 bucket policy to allow public read access to objects
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{s3_config.bucket_name}/*"],
        }
    ],
}


@asynccontextmanager
async def on_startup(app: FastAPI):
    """
    Application startup event handler.

    Notes
    -----
    This startup event runs when the application starts
    It does two things:
    1. Creates all database tables based on the defined models
    2. Ensures the S3 bucket for image storage exists with the correct policy
    """
    try:
        logger.remove()  # Remove default logger to avoid duplicate logs
        logger.add(env.LOG_FILE_PATH, level=env.LOG_LEVEL)
        logger.info("Starting Docuisine application...")
        Base.metadata.create_all(bind=engine)
        try:
            logger.info(f"Checking if S3 bucket '{s3_config.bucket_name}' exists...")
            s3_storage.head_bucket(Bucket=s3_config.bucket_name)
            logger.info(f"S3 bucket '{s3_config.bucket_name}' already exists.")
        except ClientError:
            logger.warning(
                f"S3 bucket '{s3_config.bucket_name}' does not exist. Creating bucket..."
            )
            s3_storage.create_bucket(Bucket=s3_config.bucket_name)
            s3_storage.put_bucket_policy(Bucket=s3_config.bucket_name, Policy=json.dumps(policy))
        yield
    finally:
        # Dispose of the database engine when the application shuts down
        if not callable(hasattr(engine, "dispose")):
            raise RuntimeError(
                "Database engine is not initialized. "
                "This is likely because the provided DATABASE_URL is wrong."
                f" Provided DATABASE_URL: {env.DATABASE_URL}"
            )
        else:
            await engine.dispose()


app = FastAPI(lifespan=on_startup)


@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.exception(f"{request.method} {request.url.path} failed after {duration_ms:.2f}ms")
        raise

    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.2f}ms)"
    )
    return response


app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.root.router)
app.include_router(routes.auth.router)
app.include_router(routes.user.router)
app.include_router(routes.category.router)
app.include_router(routes.store.router)
app.include_router(routes.ingredient.router)
app.include_router(routes.recipe.router)
app.include_router(routes.health.router)
app.include_router(routes.image.router)
