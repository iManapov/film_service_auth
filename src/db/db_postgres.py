from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from src.core.config import settings

db = SQLAlchemy()


def init_db():
    conn_string = f'postgresql://{settings.pg_user}:{settings.pg_pass}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db_name}'
    engine = sqlalchemy.create_engine(conn_string)
    engine.execute("CREATE SCHEMA IF NOT EXISTS auth_service;")
