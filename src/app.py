import os
import sys

from src.core.ma import ma
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.db.db_postgres import db, init_db
from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api


app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(app)
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


def register_extensions(app):
    """Register Flask extensions."""
    ma.init_app(app)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


register_extensions(app)
from src.resource.roles import Role, RoleList
api.add_resource(Role, '/role/<string:id>')
api.add_resource(RoleList, "/role/")

def main():
    init_db(app)
    app.app_context().push()
    db.create_all()
    app.run(debug=True)


if __name__ == '__main__':
    main()
