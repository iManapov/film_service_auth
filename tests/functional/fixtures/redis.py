import json
import uuid

import pytest
import aioredis

from tests.functional.settings import test_settings


@pytest.fixture(scope="session")
async def redis_blocklist():
    """
    Фикстура для установления соединения с Redis
    на время тестов (Блок-лист access-токенов)
    """
    jwt_redis_blocklist = aioredis.StrictRedis(
        host=test_settings.redis_host,
        port=test_settings.redis_port,
        db=0,
        decode_responses=True
    )
    yield jwt_redis_blocklist
    await jwt_redis_blocklist.close()

@pytest.fixture
def check_in_blocklist(redis_blocklist: aioredis.StrictRedis):
    """
    Фикстура для проверки нахождения access-токена в блоклисте
    """
    async def inner(jti: str) -> bool:
        token = await redis_blocklist.exists(jti)
        if token:
            return True
        return False
    return inner

@pytest.fixture(scope="session")
async def redis_refresh_list():
    """
    Фикстура для установления соединения с Redis
    на время тестов (Активные refresh-токены)
    """
    jwt_redis_refresh_list = aioredis.StrictRedis(
        host=test_settings.redis_host,
        port=test_settings.redis_port,
        db=1,
        decode_responses=True
    )
    yield jwt_redis_refresh_list
    await jwt_redis_refresh_list.close()

@pytest.fixture
def check_in_refresh_list(redis_refresh_list: aioredis.StrictRedis):
    """
    Фикстура для проверки нахождения refresh-токена в Redis
    """
    async def inner(jti: str, user_uuid: uuid.UUID) -> bool:
        token_identity = await redis_refresh_list.get(jti)
        if token_identity == str(user_uuid):
            return True
        return False
    return inner