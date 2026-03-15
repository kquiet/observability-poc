"""Module that support to create a FastAPI application"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api import ping, beats
from app.dataaccess.db import metadata, engine
from fastapi_metrics_prometheus.base import PrometheusMiddleware, metrics
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # drop and create for testing purpose
        async with engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)
        yield  # application starts running here
    except Exception as e:
        logger.exception('{}'.format(e))
    finally:
        await engine.dispose()

app = FastAPI(debug=False, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

# Add prometheus asgi middleware to route /metrics requests

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"{str(exc)}"},
    )

app.include_router(ping.router)
app.include_router(beats.router, prefix="/beats", tags=["beats"])
