import redis

from src.core.config import settings


# For storing inactive access tokens
jwt_redis_blocklist = redis.StrictRedis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=0,
    decode_responses=True
)

# For storing refresh tokens
jwt_redis_refresh = redis.StrictRedis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=1,
    decode_responses=True
)

# For limiting user requests rate
rate_limit_redis_pool = redis.ConnectionPool(
    host=settings.redis_host,
    port=settings.redis_port,
    db=2,
    decode_responses=True
)
