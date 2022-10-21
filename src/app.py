from flask import Flask
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.db.db_postgres import db, init_db
from src.models.users import User
from src.models.roles import Role
from src.models.user_role import UserRole
from src.models.authentication import Authentication

app = Flask(__name__)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


def main():
    init_db(app)
    app.app_context().push()
    db.create_all()
    app.run()


if __name__ == '__main__':
    main()
