import os
import sys

from src.core.ma import ma
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.db.db_postgres import db, init_db
from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api

=======
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from secrets import SystemRandom

from flask import Flask
from flask_restful import Resource, Api
from flask_security import Security
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from src.db.db_postgres import db, init_db
from src.models.user_role import UserRole
from src.models.authentication import Authentication
from src.resources.user import SignUp, Login, RefreshTokens, Logout
from src.utils import user_datastore

>>>>>>> Stashed changes

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(app)
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


def register_extensions(app):
    """Register Flask extensions."""
    ma.init_app(app)

# Конфигурация Flask-Security
app.config['SECRET_KEY'] = 'super-secret'
security = Security(app, user_datastore)

# Конфигурация Flask-JWT-Extended
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Конфигурация API Flask-restful
api = Api(app, prefix='/api/v1')
api.add_resource(SignUp, '/user/signup')
api.add_resource(Login, '/user/login')
api.add_resource(RefreshTokens, '/user/refresh')
api.add_resource(Logout, '/user/logout')

# Конфигурация Flasgger
swagger = Swagger(app)


register_extensions(app)
from src.resource.roles import Role, RoleList
api.add_resource(Role, '/role/<string:id>')
api.add_resource(RoleList, "/role/")

def main():
    init_db(app)
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
<<<<<<< Updated upstream
    app.run()
=======
    init_db(app)
    app.app_context().push()
    db.create_all()
    app.run(host='0.0.0.0', port=5000)
>>>>>>> Stashed changes


if __name__ == '__main__':
    main()
