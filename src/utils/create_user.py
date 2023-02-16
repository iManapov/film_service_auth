
import click
from flask import Flask

from src.db.db_postgres import db
from src.utils.security import get_hash
from src.utils.user_datastore import user_datastore


def init_create_user(app: Flask):
    """
    Создание консольной команды по созданию пользователя для Flask.

    app: Приложение
    """
    @app.cli.command("create-user")
    @click.argument("login")
    @click.argument("password")
    @click.argument("email")
    def create_user(password, login, email):
        user = {
            'login': login,
            'password': get_hash(password),
            'email': email,
            'first_name': 'first_name',
            'last_name': 'last_name',
            'is_administrator': True
        }
        user_datastore.create_user(**user)
        db.session.commit()
