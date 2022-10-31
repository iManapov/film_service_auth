
from http import HTTPStatus


role_test_data = [
    (
        {
            "name": "first role",
            "description": "description first role",
        },
        {
            "status": HTTPStatus.CREATED
        }
    ),

    (
        {
            "name": "second role",
            "description": "description second role",
        },
        {
            "status": HTTPStatus.CREATED
        }
    ),

    (
        {
            "name": "second role",
            "description": "description second role",
        },
        {
            "status": HTTPStatus.NOT_FOUND
        }
    ),

    (
        {
            "name": "second role",
            "description": "description second role",
            "email": "as3@sa.com"
        },
        {
            "status": HTTPStatus.BAD_REQUEST
        }
    ),

(
        {
            "name": "second role",
        },
        {
            "status": HTTPStatus.BAD_REQUEST
        }
    )
]

role_test_data_for_id = [
    (
        {
            "name": "third role",
            "description": "description third role",
        },
        {
            "status": HTTPStatus.CREATED
        },
        {
            "name": "other role",
            "description": "description other role",
        }
    ),

]