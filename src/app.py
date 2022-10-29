import os
import sys

from flask import Flask, Blueprint  # , Blueprint, jsonify, request
from flask_restful import Api
from flask_security import Security
from flask_jwt_extended import JWTManager
from flasgger import Swagger


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.extensions import ma
from src.db.db_postgres import db, init_db


app = Flask(__name__)
# bluePrint = Blueprint('api', __name__, url_prefix='/api')
# api = Api(app)
# app.register_blueprint(bluePrint)

api = Api(app, prefix='/api/v1')
swagger = Swagger(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Конфигурация Flask-JWT-Extended
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'


def register_extensions(app):
    """Register Flask extensions."""
    ma.init_app(app)


register_extensions(app)
from src.api.v1.user import SignUp, Login, RefreshTokens, Logout
from src.api.v1.roles import Roles, RoleList

from src.utils import user_datastore

# Конфигурация Flask-Security
security = Security(app, user_datastore)

# Конфигурация API Flask-restful
api.add_resource(SignUp, '/user/signup')
api.add_resource(Login, '/user/login')
api.add_resource(RefreshTokens, '/user/refresh')
api.add_resource(Logout, '/user/logout')
api.add_resource(Roles, '/role/<string:id>')
api.add_resource(RoleList, "/role/")


def main():
    init_db(app)
    app.app_context().push()
    db.create_all()
    # app.run()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
