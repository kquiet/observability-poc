from app.dataaccess.db import engine
from sqlalchemy import String
from sqlalchemy.sql import text, bindparam
from opentelemetry import trace
import logging

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


async def upsert_beats(id: int):
    with tracer.start_as_current_span("upsert_beats"):
        logger.info("upsert_beats() called")

        async with engine.begin() as conn:
            stmt = text("""INSERT INTO beats (description) VALUES (:description)
                        ON DUPLICATE KEY UPDATE
                        description=:description""").bindparams(bindparam("description", type_=String))

            await conn.execute(stmt, {"description": str(id)*2})
            await conn.commit()
            return True
    return False
