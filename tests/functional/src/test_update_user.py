import pytest

from http import HTTPStatus

from tests.functional.testdata.user import test_users, change_creds_data
from tests.functional.testdata.roles import test_roles


pytestmark = pytest.mark.asyncio

first_user_login = {
    'login': test_users[0]['login'],
    'password': test_users[0]['password']
}


@pytest.mark.parametrize(
    'user_data, expected_answer',
    change_creds_data
)
async def test_change_creds(make_post_request, make_put_request, user_data: dict, expected_answer: dict):
    """Тест для проверки API изменения данных пользователя."""

    for user_dict in test_users:
        await make_post_request("/api/v1/user/signup", user_dict)

    body, status = await make_post_request("/api/v1/user/login", first_user_login)
    assert status == HTTPStatus.OK

    access_token = body['access_token']
    user_id = body['user_id']
    headers = {"Authorization": f"Bearer {access_token}"}
    body, status = await make_put_request(f"/api/v1/user/{user_id}/change_credentials", user_data, headers=headers)
    assert status == expected_answer["status"]

    if status == HTTPStatus.OK:
        assert user_data['login'] == body['result']['login']
        assert user_data['email'] == body['result']['email']


async def test_get_login_history(make_post_request, make_get_request):
    """Тест для проверки API получений историй входа."""

    body, status = await make_post_request("/api/v1/user/login", first_user_login)
    assert status == HTTPStatus.OK

    access_token = body['access_token']
    user_id = body['user_id']
    headers = {"Authorization": f"Bearer {access_token}"}
    body, status = await make_get_request(f"/api/v1/user/{user_id}/login_history", headers=headers)

    assert status == HTTPStatus.OK
    assert len(body['result']) > 0

    _, status = await make_get_request(f"/api/v1/user/cdsdshfg/login_history", headers=headers)
    assert status == HTTPStatus.BAD_REQUEST


async def test_user_roles(make_post_request, make_get_request, make_delete_request):
    """Тест для проверки API работы с ролями пользователей."""

    role_ids = []
    for role_info in test_roles:
        body, status = await make_post_request("/api/v1/role", role_info)
        assert status == HTTPStatus.CREATED
        role_ids.append(body['id'])

    body, status = await make_post_request("/api/v1/user/login", first_user_login)
    assert status == HTTPStatus.OK

    access_token = body['access_token']
    user_id = body['user_id']
    headers = {"Authorization": f"Bearer {access_token}"}

    for role_id in role_ids:
        body, status = await make_post_request(f"/api/v1/user/{user_id}/roles/{role_id}", headers=headers)
        assert status == HTTPStatus.OK

    body, status = await make_get_request(f"/api/v1/user/{user_id}/roles", headers=headers)
    assert status == HTTPStatus.OK
    assert len(body['result']) == 2

    body, status = await make_delete_request(f"/api/v1/user/{user_id}/roles/{role_ids[0]}", headers=headers)
    assert status == HTTPStatus.OK

    body, status = await make_get_request(f"/api/v1/user/{user_id}/roles", headers=headers)
    assert status == HTTPStatus.OK
    assert len(body['result']) == 1

    _, status = await make_post_request(f"/api/v1/user/dcdsfdsdsf/roles/dsfdfsddsf", headers=headers)
    assert status == HTTPStatus.BAD_REQUEST

    _, status = await make_delete_request(f"/api/v1/user/dcdsfdsdsf/roles/dsfdfsddsf", headers=headers)
    assert status == HTTPStatus.BAD_REQUEST

    body, status = await make_get_request(f"/api/v1/user/dfdsfd-fdds-dsfds/roles", headers=headers)
    assert status == HTTPStatus.BAD_REQUEST
