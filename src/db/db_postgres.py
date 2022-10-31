from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from src.core.config import settings

db = SQLAlchemy()


def init_db(app: Flask):
    conn_string = f'postgresql://{settings.pg_user}:{settings.pg_pass}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db_name}'
    engine = sqlalchemy.create_engine(conn_string)
    engine.execute("CREATE SCHEMA IF NOT EXISTS auth_service;")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{conn_string}?options=-c%20search_path=auth_service'
    db.init_app(app)
