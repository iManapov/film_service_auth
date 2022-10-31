from http import HTTPStatus


user_test_data = [
    (
        {
            "login": "121",
            "password": "121",
            "email": "as121@sa.com",
            "first_name": "Bob",
            "last_name": "Smith"
        },
        {
            "status": HTTPStatus.CREATED
        }
    ),

    (
        {
            "login": "1",
            "password": "1",
            "email": "as3@sa.com",
            "first_name": "Bob",
            "last_name": "Smith"
        },
        {
            "status": HTTPStatus.CREATED
        }
    ),

    (
        {
            "login": "3",
            "password": "3",
        },
        {
            "status": HTTPStatus.BAD_REQUEST
        }
    ),

    (
        {
            "login": "3",
            "password": "3",
            "email": "as3@sa.com",
        },
        {
            "status": HTTPStatus.BAD_REQUEST
        }
    ),

    (
        {
            "login": "11",
            "password": "3",
            "email": "as4@sa.com",
        },
        {
            "status": HTTPStatus.BAD_REQUEST
        }
    ),
]

login_test_data = [
    (
        {
            "login": "121",
            "password": "121",
        },
        {
            "status": HTTPStatus.OK
        }
    ),

    (
        {
            "login": "qqq",
            "password": "8",
        },
        {
            "status": HTTPStatus.BAD_REQUEST
        }
    ),
]