from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.core.config import settings

db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{settings.pg_user}:{settings.pg_pass}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db_name}'
    db.init_app(app)
