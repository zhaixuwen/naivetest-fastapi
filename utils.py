from database import SessionLocal
from loguru import logger
import aioredis
from config import REDIS_HOST, REDIS_PASSWORD

logger = logger


def get_db():
    # try:
    #     db = SessionLocal()
    #     yield db
    # finally:
    #     db.close()
    with SessionLocal() as db:
        yield db


async def get_redis():
    redis = await aioredis.from_url(f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}/0", decode_responses=True)
    return redis
