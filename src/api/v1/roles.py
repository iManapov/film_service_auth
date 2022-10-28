from flask import request
from flask_restful import Resource, reqparse

from src.models.roles import Role
from src.schemas.roles import RoleSchema

ROLE_NOT_FOUND = "Role not found."
ROLE_NAME_AlREADY_EXISTS = 'Role "{}" already exists'


# role_ns = Namespace('role', description='Role related operations')
# roles_ns = Namespace('roles', description='Role related operations')

role_schema = RoleSchema()
role_list_schema = RoleSchema(many=True)


#Model required by flask_restplus for expect
# role = roles_ns.model('Role', {
#     'name': fields.String('Name of the Role'),
#     'description': fields.String
# })


class Roles(Resource):

    def get(self, id):
        role_data = Role.find_by_id(id)
        if role_data:
            return role_schema.dump(role_data)
        return {'message': ROLE_NOT_FOUND}, 404

    def delete(self, id):
        role_data = Role.find_by_id(id)
        if role_data:
            role_data.delete_from_db()
            return {'message': "Role Deleted successfully"}, 200
        return {'message': ROLE_NOT_FOUND}, 404

    def put(self, id):
        role_data = Role.find_by_id(id)
        role_json = request.get_json()

        if role_data:
            role_data.name = role_json['name']
            role_data.description = role_json['description']
        else:
            return {'message': ROLE_NOT_FOUND}, 404

        role_data.save_to_db()
        return role_schema.dump(role_data), 200


class RoleList(Resource):
    def get(self):
        return role_list_schema.dump(Role.find_all()), 200

    def post(self):
        role_json = request.get_json()
        role_data = role_schema.load(role_json)
        if role_data.find_by_name(role_json['name']):
            return {'message': ROLE_NAME_AlREADY_EXISTS.format(role_json['name'])}, 404
        else:
            role_data.save_to_db()

        return role_schema.dump(role_data), 201
