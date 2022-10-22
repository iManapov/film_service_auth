import os
import sys

from src.core.ma import ma
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.db.db_postgres import db, init_db
from flask import Flask, Blueprint, jsonify, request
from flask_restplus import Api

from src.resource.roles import Role, RoleList, roles_ns, role_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(bluePrint, doc='/doc', title='Sample Flask-RestPlus Application')
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(role_ns)
api.add_namespace(roles_ns)

role_ns.add_resource(Role, '/<int:id>')
roles_ns.add_resource(RoleList, "")

def register_extensions(app):
    """Register Flask extensions."""
    ma.init_app(app)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


# def do_the_roles(name: str, description: str = None):
#     from src.models.roles import Role, RoleSchema
#     role_schema = RoleSchema()
#     role = Role(name=name, description=description)
#     db.session.add(role)
#     db.session.commit()
#     role_schema.dump(role)
#     return role_schema.id
#
#
# def show_the_login_form():
#     pass
#
#
# @app.route('/roles', methods=['GET', 'POST'])
# def roles():
#     response = 'Response: '
#     id = ''
#     if request.method == 'POST':
#         id = do_the_roles(request.args.get('name', ''), request.args.get('description', ''))
#     else:
#         show_the_login_form()
#     return response + id

@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


def main():
    init_db(app)
    ma.init_app(app)
    app.app_context().push()
    db.create_all()
    app.run(debug=True)


if __name__ == '__main__':
    main()
