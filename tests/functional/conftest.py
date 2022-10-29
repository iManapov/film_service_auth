import random
import uuid

import aiohttp
import asyncio
import json

import aioredis
import pytest
from aioredis import Redis
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import connection as _connection

from tests.functional.settings import test_settings
from tests.functional.testdata.film_data import es_film_data
from tests.functional.testdata.genre_data import es_genre_data
from tests.functional.testdata.es_mapping import es_movies_index, es_genres_index, es_persons_index
from tests.functional.testdata.person_data import es_data_persons


@pytest.fixture(scope="session")
def event_loop():
    """
    Переопределенная стандартная фикстура
    для создания цикла событий
    на время выполнения тестов
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def pg_client():
    """
    Фикстура для установления соединения с ES
    на время тестов
    """
    dsl = test_settings.pg_dsn
    client = psycopg2.connect(dsl, cursor_factory=DictCursor)
    yield client
    await client.close()


@pytest.fixture(autouse=True, scope="session")
async def pg_clear_data(pg_conn: _connection):
    conn = pg_conn
    curs = conn.cursor()
    curs.curs.execute("TRUNCATE auth_service.roles, auth_service.authentication, auth_service.user_role, "
                      "auth_service.users")


async def es_write_data_to_index(
    es_client: AsyncElasticsearch,
    es_index_name: str,
    es_index_schema: dict,
    data: list[dict],
):
    """
    Функция для записи тестовых данных в индекс

    :param es_client: фикстура клиента elasticsearch
    :param es_index_name: название индекса в elasticsearch
    :param es_index_schema: схема индекса в elasticsearch
    :param data: тестовые данные
    """

    bulk_query = []
    list_with_films_id = []
    for row in data:
        bulk_query.extend(
            [
                json.dumps(
                    {
                        "index": {
                            "_index": es_index_name,
                            "_id": row[test_settings.elastic_id_field],
                        }
                    }
                ),
                json.dumps(row),
            ]
        )
        if es_index_name == es_movies_index:
            list_with_films_id.append(row['id'])
    str_query = "\n".join(bulk_query) + "\n"
    print(f"Writing index {es_index_name}")
    if not await es_client.indices.exists(index=es_index_name):
        await es_client.indices.create(index=es_index_name, body=es_index_schema)
    print(f"Writing index {es_index_name}")
    response = await es_client.bulk(str_query, refresh=True)
    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")
    return list_with_films_id


#@pytest.fixture(autouse=True, scope="session")
async def es_write_data(es_client: AsyncElasticsearch):
    """
    Фикстура для заполнения ES данными
    Срабатывает один раз в начале тестов
    """

    list_with_films_id = await es_write_data_to_index(
        es_client, test_settings.elastic_movies_index, es_movies_index, es_film_data
    )
    await es_write_data_to_index(
        es_client, test_settings.elastic_genres_index, es_genres_index, es_genre_data
    )


@pytest.fixture(scope="session")
async def http_session():
    """
    Фикстура для установления соединения по
    HTTP на время тестов
    """
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения запроса к API
    """

    async def inner(url: str, query_data: dict = None):
        url = test_settings.service_url + url
        async with http_session.get(url, params=query_data) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner

@pytest.fixture
def make_post_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения запроса к API
    """

    async def inner(url: str, query_data: dict = None):
        url = test_settings.service_url + url
        async with http_session.post(url, data=query_data) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner

@pytest.fixture
def make_put_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения запроса к API
    """

    async def inner(url: str, query_data: dict = None):
        url = test_settings.service_url + url
        async with http_session.put(url, data=query_data) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner

@pytest.fixture
def make_delete_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения запроса к API
    """

    async def inner(url: str):
        url = test_settings.service_url + url
        async with http_session.delete(url) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner

@pytest.fixture(scope="session")
async def redis_client():
    """
    Фикстура для установления соединения с Redis
    на время тестов
    """
    client = await aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port), minsize=10, maxsize=20
    )
    yield client
    client.close()
    await client.wait_closed()


@pytest.fixture
def check_cache(redis_client: Redis):
    """
    Фикстура для проверки результата запроса в кеше
    """

    async def inner(url: str):
        cache_data = await redis_client.get(url)
        if cache_data:
            return json.loads(cache_data)
        return None

    return inner

