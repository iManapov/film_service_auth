import pytest

from http import HTTPStatus

from tests.functional.testdata.roles import role_test_data, role_test_data_for_id

pytestmark = pytest.mark.asyncio
invalid_id = '26326d5a-592e-11ed-9b6a-0242ac120002'


@pytest.mark.parametrize(
    'role_data, expected_answer',
    role_test_data
)
async def test_roles(make_post_request,
                     make_get_request,
                     execute_sql,
                     role_data: dict,
                     expected_answer: dict):
    """
    Тест для проверки API создания и получения ролей
    """
    body, status = await make_post_request("/api/v1/role/", role_data)
    assert status == expected_answer["status"]

    if status == HTTPStatus.CREATED:
        body, status = await make_get_request("/api/v1/role/")
        assert status == HTTPStatus.OK
        assert role_data["name"] == body[-1]["name"]
        assert role_data["description"] == body[-1]["description"]


@pytest.mark.parametrize(
    'role_data, expected_answer, new_role_data',
    role_test_data_for_id
)
async def test_roles_id(make_post_request,
                        make_get_request,
                        make_delete_request,
                        make_put_request,
                        execute_sql,
                        role_data: dict,
                        expected_answer: dict,
                        new_role_data: dict):
    """
    Тест для проверки API создания и получения ролей по id
    """

    async def get(id):
        body, status = await make_get_request(f"/api/v1/role/{id}")
        assert status == HTTPStatus.OK
        assert id == body["id"]
        body, status = await make_get_request(f"/api/v1/role/{invalid_id}")
        assert status == HTTPStatus.NOT_FOUND

    async def delete(id):
        body, status = await make_delete_request(f"/api/v1/role/{id}")
        assert status == HTTPStatus.OK
        body, status = await make_delete_request(f"/api/v1/role/{invalid_id}")
        assert status == HTTPStatus.NOT_FOUND

    async def put(id):
        body, status = await make_put_request(f"/api/v1/role/{id}", new_role_data)
        assert status == HTTPStatus.OK
        assert body['name'] == new_role_data['name']
        assert body['description'] == new_role_data['description']
        body, status = await make_put_request(f"/api/v1/role/{invalid_id}", new_role_data)
        assert status == HTTPStatus.NOT_FOUND

    body, status = await make_post_request("/api/v1/role/", role_data)
    assert status == HTTPStatus.CREATED
    role_id = body['id']

    await get(role_id)
    await put(role_id)
    await delete(role_id)
