import os
import sys

from flask import Flask, Blueprint
from flask_security import Security
from flasgger import Swagger

from src.utils.create_user import init_create_user

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.extensions import ma, jwt
from src.db.db_postgres import db, init_db
from src.models.authentication import Authentication
from src.utils import user_datastore
from src.core.config import settings
from src.api.v1.resources import api_v1


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Конфигурация Flask-JWT-Extended
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'

# Конфигурация Swagger
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'

swagger = Swagger(app, config=swagger_config)
security = Security(app, user_datastore)

auth_service = Blueprint('auth_service', __name__, url_prefix='/')
auth_service.register_blueprint(api_v1)
app.register_blueprint(auth_service)


def register_extensions(app):
    """Register Flask extensions."""
    ma.init_app(app)
    jwt.init_app(app)
    init_create_user(app)


def prepare_start():
    register_extensions(app)
    init_db(app)
    app.app_context().push()
    db.create_all()


prepare_start()


if __name__ == '__main__':
    app.run(host=settings.service_host, port=settings.service_port, debug=settings.debug)
