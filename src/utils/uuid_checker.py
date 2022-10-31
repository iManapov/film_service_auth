from uuid import UUID


def is_uuid(uuid_to_test):
    """Проверка на uuid."""

    try:
        UUID(str(uuid_to_test))
        return True
    except ValueError:
        return False
