import jwt

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

    Проверяется:
    1) статус ответа
    2) присутствие созданного пользователя в Postgres, если статус ответа API - CREATED
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
                          execute_sql,
                          check_in_refresh_list,
                          user_data: dict,
                          expected_answer: dict):
    """
    Тест для проверки API входа и
    получения пары access и refresh токенов

    Проверяется:
    1) статус ответа
    2) присутствие выданного refresh-токена в redis, если статус ответа API - OK
    """
    body, status = await make_post_request("/api/v1/user/login", user_data)
    assert status == expected_answer["status"]

    if status == HTTPStatus.OK:
        jti = jwt.decode(body["refresh_token"], options={"verify_signature": False})["jti"]
        user = await execute_sql(
            f"SELECT id FROM auth_service.users WHERE login='{user_data['login']}'"
        )
        assert await check_in_refresh_list(jti, user) == True

@pytest.mark.parametrize(
    'user_data, expected_answer',
    login_test_data
)
async def test_user_refresh(make_post_request,
                            execute_sql,
                            check_in_refresh_list,
                            user_data: dict,
                            expected_answer: dict):
    """
    Тест для проверки получения новой пары access и refresh токенов
    с помощью refresh-токена

    Проверяется:
    1) статус ответа
    2) отсутствие старого refresh-токена в redis, если статус ответа API - ОК
    3) присутствие нового refresh-токена в redis, если статус ответа API - ОК
    """
    body, status = await make_post_request("/api/v1/user/login", req_body=user_data)

    if status == HTTPStatus.OK:
        old_jti = jwt.decode(body["refresh_token"],
                             options={"verify_signature": False})["jti"]
        user = await execute_sql(
            f"SELECT id FROM auth_service.users WHERE login='{user_data['login']}'"
        )
        headers = {
            "Authorization": f"Bearer {body['refresh_token']}"
        }

        body, status = await make_post_request("/api/v1/user/refresh", headers=headers)
        new_jti = jwt.decode(body["refresh_token"],
                             options={"verify_signature": False})["jti"]

        assert status == expected_answer["status"]
        assert await check_in_refresh_list(new_jti, user) == True
        assert await check_in_refresh_list(old_jti, user) == False

@pytest.mark.parametrize(
    'user_data, expected_answer',
    login_test_data
)
async def test_user_logout(make_post_request,
                           check_in_refresh_list,
                           check_in_blocklist,
                           make_delete_request,
                           execute_sql,
                           user_data: dict,
                           expected_answer: dict):
    """
    Тест для проверки процедуры выхода пользователя из системы

    Проверяется:
    1) статус ответа
    2) отсутствие refresh-токена в redis, если статус ответа API - ОК
    3) присутствие access-токена в блок-листе redis, если статус ответа API - ОК
    """
    body, status = await make_post_request("/api/v1/user/login", req_body=user_data)

    if status == HTTPStatus.OK:
        user = await execute_sql(
            f"SELECT id FROM auth_service.users WHERE login='{user_data['login']}'"
        )
        headers = {
            "Authorization": f"Bearer {body['refresh_token']}"
        }

        body, status = await make_post_request("/api/v1/user/refresh", headers=headers)
        jti = jwt.decode(body["access_token"],
                         options={"verify_signature": False})["jti"]
        jti_refresh = jwt.decode(body["access_token"],
                         options={"verify_signature": False})["jti_refresh"]

        if status == HTTPStatus.OK:
            headers = {
                "Authorization": f"Bearer {body['access_token']}"
            }
            body, status = await make_delete_request("/api/v1/user/logout", headers=headers)

            assert status == expected_answer["status"]
            assert await check_in_blocklist(jti) == True
            assert await check_in_refresh_list(jti_refresh, user) == False
