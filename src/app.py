import os
import sys

from flask import Flask
from flask_restful import Api
from flask_security import Security
from flask_jwt_extended import JWTManager
from flasgger import Swagger


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.extensions import ma, jwt
from src.db.db_postgres import db, init_db
from src.api.v1.user import SignUp, Login, RefreshTokens, Logout, ChangeCreds, \
    LoginHistory, UserRoles, ChangeUserRoles
from src.api.v1.roles import Roles, RoleList
from src.models.authentication import Authentication
from src.utils import user_datastore
from src.core.config import settings


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Конфигурация Flask-JWT-Extended
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'


api = Api(app, prefix='/api/v1')
swagger = Swagger(app)
jwt = JWTManager(app)
security = Security(app, user_datastore)


# Конфигурация API Flask-restful
api.add_resource(SignUp, '/user/signup')
api.add_resource(Login, '/user/login')
api.add_resource(RefreshTokens, '/user/refresh')
api.add_resource(Logout, '/user/logout')
api.add_resource(ChangeCreds, '/user/<string:user_id>/change_credentials')
api.add_resource(LoginHistory, '/user/<string:user_id>/login_history')
api.add_resource(UserRoles, '/user/<string:user_id>/roles')
api.add_resource(ChangeUserRoles, '/user/<string:user_id>/roles/<string:role_id>')

api.add_resource(Roles, '/role/<string:id>')
api.add_resource(RoleList, "/role/")


def register_extensions(app):
    """Register Flask extensions."""
    ma.init_app(app)
    jwt.init_app(app)


def prepare_start():
    register_extensions(app)
    init_db(app)
    app.app_context().push()
    db.create_all()


prepare_start()


if __name__ == '__main__':
    app.run(host=settings.service_host, port=settings.service_port, debug=settings.debug)
