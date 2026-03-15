from fastapi import APIRouter, Path
from app.service.beats import process_beats
from opentelemetry import trace
import logging

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
router = APIRouter()


@router.get("/{id}/")
async def fire_beats(id: int = Path(..., gt=0),):
    with tracer.start_as_current_span("fire_beats"):
        logger.info("fire_beats() called")
        result = await process_beats(id)
        if result:
            return '{"result":"ok"}'
        else:
            return '{"result":"fail"}'
