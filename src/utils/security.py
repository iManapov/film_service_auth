from functools import wraps
from http.client import FORBIDDEN

import string
from secrets import choice as secrets_choice
import bcrypt
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def get_hash(password: str) -> bytes:
    """
    Returns hash for password

    :param password: password for hashing
    """

    bytes_ = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_ = bcrypt.hashpw(bytes_, salt)
    return hash_


def check_password(password: str, stored_hash: bytes) -> bool:
    """
    Checks password with stored hash

    :param password: password
    :param stored_hash: stored hash
    """

    bytes_ = password.encode('utf-8')
    return bcrypt.checkpw(bytes_, stored_hash)


def admin_required():
    """
    Checks is user admin
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return {'msg': 'Admins only!'}, FORBIDDEN

        return decorator

    return wrapper


def generate_random_string():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets_choice(alphabet) for _ in range(16))
