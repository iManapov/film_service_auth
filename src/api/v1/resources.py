from flask_restful import Api
from flask import Blueprint

from src.api.v1.roles import Roles, RoleList
from src.api.v1.user import SignUp, Login, RefreshTokens, Logout, ChangeCreds, LoginHistory, UserRoles, ChangeUserRoles

api_v1 = Blueprint('api_v1', __name__, url_prefix='api/v1')

api = Api(api_v1)

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
