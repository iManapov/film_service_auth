from functools import wraps
from http.client import FORBIDDEN

import bcrypt
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def get_hash(password: str) -> bytes:
    """
    Получение соли для хеширования и самого хэша

    @param password: пароль для хэширования
    """
    bytes_ = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_ = bcrypt.hashpw(bytes_, salt)
    return hash_


def check_password(password: str, stored_hash: bytes) -> bool:
    """
    Проверка соответствия хэша полученного пароля хранимому хэшу

    @param password: полученный пароль для сравнения с хэшем
    @param stored_hash: хранимый хэш
    """
    bytes_ = password.encode('utf-8')
    return bcrypt.checkpw(bytes_, stored_hash)


def admin_required():
    """
    Проверка пользователя на наличие прав администратора
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
