import bcrypt


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
