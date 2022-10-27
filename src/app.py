<<<<<<< Updated upstream
from flask import Flask

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


def main():
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
