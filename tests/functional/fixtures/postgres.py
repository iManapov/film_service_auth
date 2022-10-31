import sqlalchemy
import pytest

from tests.functional.settings import test_settings


@pytest.fixture(scope="session")
async def postgre_connection():
    """
    Фикстура для установления соединения
    с Postgre
    """
    conn_string = (f"postgresql://{test_settings.pg_user}:{test_settings.pg_pass}"
                   f"@{test_settings.pg_host}:{test_settings.pg_port}/"
                   f"{test_settings.pg_db_name}"
                   )
    engine = sqlalchemy.create_engine(conn_string)

    yield engine
    engine.dispose()

@pytest.fixture
def execute_sql(postgre_connection: sqlalchemy.engine.base.Engine):
    """
    Фикстура для SQL-запроса к Postgre
    """
    async def inner(query: str) -> str:
        result = postgre_connection.execute(query).scalar()
        return result

    return inner

@pytest.fixture(autouse=True, scope="session")
async def pg_clear_data(postgre_connection: sqlalchemy.engine.base.Engine):
    """
    Фикстура для удаления данных из таблиц users и roles в Postgres
    Срабатывает один раз в начале тестов
    """
    postgre_connection.execute("DELETE FROM auth_service.users CASCADE;")
    postgre_connection.execute("DELETE FROM auth_service.role CASCADE;")
    postgre_connection.execute("DELETE FROM auth_service.user_role CASCADE;")