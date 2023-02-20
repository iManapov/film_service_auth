import logging
import os
import sys

import logstash
import sentry_sdk
from http import HTTPStatus

from flask import Flask, Blueprint, request
from flask_migrate import Migrate
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from opentelemetry.instrumentation.flask import FlaskInstrumentor


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.extensions import ma, jwt, migrate, limiter
from src.db.db_postgres import db, init_db
from src.utils import user_datastore
from src.core.config import settings, yandex, vk, google, mail
from src.api.v1.resources import api_v1
from src.utils.create_user import init_create_user
from src.utils.tracing import configure_tracer
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(dsn=settings.sentry_dsn,
                integrations=[FlaskIntegration()], traces_sample_rate=1.0)


app = Flask(__name__)

app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.INFO)
logstash_handler = logstash.LogstashHandler('logstash', 5044, version=1)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


app.logger.addFilter(RequestIdFilter())
app.logger.addHandler(logstash_handler)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["SECRET_KEY"] = "super-secret"


swagger_config = Swagger.DEFAULT_CONFIG
swagger_config["swagger_ui_bundle_js"] = "//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"
swagger_config["swagger_ui_standalone_preset_js"] = "//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js"
swagger_config["jquery_js"] = "//unpkg.com/jquery@2.2.4/dist/jquery.min.js"
swagger_config["swagger_ui_css"] = "//unpkg.com/swagger-ui-dist@3/swagger-ui.css"

swagger = Swagger(app, config=swagger_config)
security = Security(app, user_datastore)


conn_string = f"postgresql://{settings.pg_user}:{settings.pg_pass}@{settings.pg_host}:{settings.pg_port}/{settings.pg_db_name}"
app.config["SQLALCHEMY_DATABASE_URI"] = f"{conn_string}?options=-c%20search_path=auth_service"

# Конфигурация Oauth
app.config['OAUTH_CREDENTIALS'] = {
    'yandex': {
        'id': yandex.id,
        'secret': yandex.secret,
    },
    'google': {
        'id': google.id,
        'secret': google.secret
    },
    'vk': {
        'id': vk.id,
        'secret': vk.secret
    },
    'mail': {
        'id': mail.id,
        'secret': mail.secret
    },
}

auth_service = Blueprint("auth_service", __name__, url_prefix="/")
auth_service.register_blueprint(api_v1)
app.register_blueprint(auth_service)

limiter.exempt(auth_service)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return {"error": 'Request id header (X-Request-Id) is missing'}, HTTPStatus.BAD_REQUEST


def register_extensions(app):
    """Register Flask extensions."""
    ma.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    init_create_user(app)
    if settings.enable_tracer:
        configure_tracer()
        FlaskInstrumentor().instrument_app(app)


def prepare_start():
    register_extensions(app)
    init_db()
    app.app_context().push()


prepare_start()


if __name__ == "__main__":
    app.run(host=settings.service_host, port=settings.service_port, debug=settings.debug)
