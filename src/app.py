import os
import sys

from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from src.utils.create_user import init_create_user

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.extensions import ma, jwt, migrate
from src.db.db_postgres import db, init_db
from src.models.authentication import Authentication
from src.utils import user_datastore
from src.core.config import settings
from src.api.v1.resources import api_v1


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Конфигурация Flask-JWT-Extended
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["SECRET_KEY"] = "super-secret"

# Конфигурация Swagger
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config["swagger_ui_bundle_js"] = "//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"
swagger_config["swagger_ui_standalone_preset_js"] = "//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js"
swagger_config["jquery_js"] = "//unpkg.com/jquery@2.2.4/dist/jquery.min.js"
swagger_config["swagger_ui_css"] = "//unpkg.com/swagger-ui-dist@3/swagger-ui.css"

swagger = Swagger(app, config=swagger_config)
security = Security(app, user_datastore)

conn_string = f"postgresql://{settings.pg_user}:{settings.pg_pass}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db_name}"
app.config["SQLALCHEMY_DATABASE_URI"] = f"{conn_string}?options=-c%20search_path=auth_service"

auth_service = Blueprint("auth_service", __name__, url_prefix="/")
auth_service.register_blueprint(api_v1)
app.register_blueprint(auth_service)


def register_extensions(app):
    """Register Flask extensions."""
    ma.init_app(app)
    jwt.init_app(app)
<<<<<<< HEAD
    db.init_app(app)
    migrate.init_app(app, db)
=======
    init_create_user(app)
>>>>>>> 6ba477b728f3cda12084fa038ff9c441ed79fbbc


def prepare_start():
    register_extensions(app)
    init_db()
    app.app_context().push()


prepare_start()


if __name__ == "__main__":
    app.run(host=settings.service_host, port=settings.service_port, debug=settings.debug)
