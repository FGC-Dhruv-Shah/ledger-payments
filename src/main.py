"""Meridian Pay ledger & payments API — application entrypoint."""

import logging

from fastapi import FastAPI

from .config import get_settings
from .routes import payments, reports

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Core payments and transaction ledger service for Meridian Pay.",
)

app.include_router(payments.router)
app.include_router(reports.router)


@app.get("/health", tags=["system"])
def health() -> dict:
    return {
        "status": "ok",
        "environment": settings.environment,
        "version": settings.api_version,
    }
