from typing import Union

from fastapi import FastAPI

from docuisine.routes import user

from .core.config import env
from .schemas import HealthCheck, Status

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health", response_model=HealthCheck)
def health_check():
    return HealthCheck(
        status=Status.HEALTHY,
        commit_hash=env.COMMIT_HASH,
        version=env.VERSION,
    )


app.include_router(user.router)
