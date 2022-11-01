import pytest
import aiohttp

from tests.functional.settings import test_settings


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
def make_post_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения POST-запроса к API
    """
    async def inner(url: str, req_body: dict = None, headers: dict = None):
        url = test_settings.service_url + url
        async with http_session.post(url, json=req_body, headers=headers) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner


@pytest.fixture
def make_put_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения PUT-запроса к API
    """
    async def inner(url: str, req_body: dict = None, headers: str = None):
        url = test_settings.service_url + url
        async with http_session.put(url, json=req_body, headers=headers) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner


@pytest.fixture
def make_get_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения GET-запроса к API
    """
    async def inner(url: str, headers: str = None):
        url = test_settings.service_url + url
        async with http_session.get(url, headers=headers) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner


@pytest.fixture
def make_delete_request(http_session: aiohttp.ClientSession):
    """
    Фикстура для выполнения DELETE-запроса к API
    """
    async def inner(url: str, headers: str = None):
        url = test_settings.service_url + url
        async with http_session.delete(url, headers=headers) as response:
            body = await response.json()
            status = response.status
            return body, status

    return inner