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


test_users = [
    {
        "login": "test1",
        "password": "pswd1",
        "email": "test1@sa.com",
        "first_name": "Bob1",
        "last_name": "Smith1"
    },
    {
        "login": "test2",
        "password": "pswd2",
        "email": "test2@sa.com",
        "first_name": "Bob2",
        "last_name": "Smith2"
    }
]


change_creds_data = [
    (
        {
            "login": "test3",
            "password": "pswd2",
            "email": "test3@sa.com",
            "first_name": "Bob1",
            "last_name": "Smith1"
        },
        {
            "status": HTTPStatus.OK
        }
    ),
    (
        {
            "login": "test2",
            "password": "pswd1",
            "email": "test1@sa.com",
            "first_name": "Bob1",
            "last_name": "Smith1"
        },
        {
            "status": HTTPStatus.BAD_REQUEST
        }
    )
]