import uuid

from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_limiter.util import get_remote_address


def get_user_uuid() -> uuid.UUID:
    """Returns user id"""

    claims = get_jwt()
    return claims["user_uuid"]


def get_key_func() -> str:
    if verify_jwt_in_request(optional=True, verify_type=False):
        return get_user_uuid()
    return get_remote_address()
