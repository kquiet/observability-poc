"""Module that support to get environment variables"""
import os
from datetime import datetime as dt
from sqlalchemy import Column, Integer, String, Table, MetaData, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

load_dotenv()

# SQLAlchemy
engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    pool_size=2,
    max_overflow=2,
    pool_recycle=300,
    echo=True,
    echo_pool=True,
)
metadata = MetaData()
beats = Table(
    "beats",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("description", String(50)),
    Column(
        "create_date",
        DateTime,
        default=dt.utcnow(),
        server_default=func.now()
    ),
)
