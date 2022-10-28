from typing import Optional

import redis

from src.core.config import settings

# для хранения невалидных access-токенов
jwt_redis_blocklist = redis.StrictRedis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=0,
    decode_responses=True
)
