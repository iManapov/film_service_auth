from typing import Optional

import redis

from src.core.config import settings

# для хранения отозванных access-токенов
jwt_redis_blocklist = redis.StrictRedis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=0,
    decode_responses=True
)

# для хранения refresh-токенов
jwt_redis_refresh = redis.StrictRedis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=1,
    decode_responses=True
)