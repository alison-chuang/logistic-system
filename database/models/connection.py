import os
import redis

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

class Base(DeclarativeBase):
    pass

engine = create_engine(
    os.getenv("DB_URL"),
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
)

redis_conn = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), decode_responses=True)
