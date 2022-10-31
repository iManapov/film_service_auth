import pytest
import sqlalchemy

from http import HTTPStatus

from tests.functional.testdata.user import user_test_data, login_test_data

from tests.functional.settings import test_settings


pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize(
    'user_data, expected_answer',
    user_test_data
)
async def test_user_signup(make_post_request,
                           execute_sql,
                           user_data: dict,
                           expected_answer: dict):
    """
    Тест для проверки API регистрации пользователя
    """
    body, status = await make_post_request("/api/v1/user/signup", user_data)
    assert status == expected_answer["status"]

    if status == HTTPStatus.CREATED:
        user = await execute_sql(
            f"SELECT login FROM auth_service.users WHERE login='{user_data['login']}'"
        )
        assert user_data["login"] == user
        assert user == body["user"]


@pytest.mark.parametrize(
    'user_data, expected_answer',
    login_test_data
)
async def test_user_login(make_post_request,
                          user_data: dict,
                          expected_answer: dict):
    """
    Тест для проверки API входа и
    получения пары access и refresh токенов
    """
    body, status = await make_post_request("/api/v1/user/login", user_data)
    assert status == expected_answer["status"]