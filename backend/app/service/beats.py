from app.dataaccess.beats import upsert_beats
from opentelemetry import trace
import logging

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


async def process_beats(id: int):
    result = False
    with tracer.start_as_current_span("process_beats"):
        logger.info("process_beats() called")
        check_id(id)
        result = await upsert_beats(id)
    return result


def check_id(id: int):
    with tracer.start_as_current_span("check_id"):
        if (id == 777):
            logger.warning("lucky number fired!")
            raise ValueError("value == 777")
