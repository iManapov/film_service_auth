from datetime import timedelta
from http import HTTPStatus

from flask_jwt_extended import create_refresh_token, get_jti, create_access_token

from src.db.db_postgres import db
from src.db.db_redis import jwt_redis_refresh
from src.models.authentication import Authentication

REFRESH_EXPIRES = timedelta(minutes=2)


def create_and_output_tokens(user, user_agent):
    """
    Creates token and returns them as JSON

    :param user: User object
    :param user_agent: user agent information
    :return: tokens
    """
    refresh_token = create_refresh_token(identity=user.id,
                                         additional_claims={
                                             "user_uuid": user.id
                                         })
    auth_hist = Authentication(user_id=user.id, user_agent=user_agent)
    db.session.add(auth_hist)
    db.session.commit()
    jti_refresh = get_jti(refresh_token)
    roles = [role.name for role in user.roles]
    additional_claims = {
        "jti_refresh": jti_refresh,
        "user_uuid": user.id,
        "is_administrator": user.is_administrator,
        "roles": roles
    }
    access_token = create_access_token(identity=user.id,
                                       additional_claims=additional_claims)
    jwt_redis_refresh.set(get_jti(refresh_token), str(user.id), ex=REFRESH_EXPIRES)

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": str(user.id)}, HTTPStatus.OK
