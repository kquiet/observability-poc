"""Module that support to create a FastPI router"""
from fastapi import APIRouter
import logging
import random
import time

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/ping")
async def ping():
    logger.info("ping() called")
    return {"ping": "pong"}


@router.get("/slowping")
async def slowping():
    logger.info("slowping() called")
    wait_time = random.uniform(0.5, 1.5)
    time.sleep(wait_time)
    return {"slowping": "pong"}
