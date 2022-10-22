
from flask import request
from flask_restplus import Resource, fields, Namespace

from src.models.roles import Roles
from src.schemas.roles import RolesSchema

ROLE_NOT_FOUND = "Role not found."


role_ns = Namespace('role', description='Role related operations')
roles_ns = Namespace('roles', description='Roles related operations')

role_schema = RolesSchema()
role_list_schema = RolesSchema(many=True)

#Model required by flask_restplus for expect
role = roles_ns.model('Roles', {
    'name': fields.String('Name of the Role'),
    'description': fields.String
})


class Role(Resource):

    def get(self, id):
        role_data = Roles.find_by_id(id)
        if role_data:
            return role_schema.dump(role_data)
        return {'message': ROLE_NOT_FOUND}, 404

    def delete(self,id):
        role_data = Roles.find_by_id(id)
        if role_data:
            role_data.delete_from_db()
            return {'message': "Role Deleted successfully"}, 200
        return {'message': ROLE_NOT_FOUND}, 404

    @role_ns.expect(role)
    def put(self, id):
        role_data = Roles.find_by_id(id)
        role_json = request.get_json()

        if role_data:
            role_data.name = role_json['name']
            role_data.description = role_json['description']
        else:
            role_data = role_schema.load(role_json)

        role_data.save_to_db()
        return role_schema.dump(role_data), 200


class RoleList(Resource):
    @roles_ns.doc('Get all the Roles')
    def get(self):
        return role_list_schema.dump(Roles.find_all()), 200

    @roles_ns.expect(role)
    @roles_ns.doc('Create an Role')
    def post(self):
        role_json = request.get_json()
        role_data = role_schema.load(role_json)
        role_data.save_to_db()

        return role_schema.dump(role_data), 201
