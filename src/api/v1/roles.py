from flask import request
from flask_restful import Resource, reqparse
from marshmallow import ValidationError

from src.models.roles import Role
from src.schemas.roles import RoleSchema

ROLE_NOT_FOUND = "Role is not found."
ROLE_NAME_AlREADY_EXISTS = 'Role "{}" already exists'

role_schema = RoleSchema()
role_list_schema = RoleSchema(many=True)


class Roles(Resource):
    """
    API-view для получения, изменения, удаления конкретной роли
    """
    def get(self, id):
        """
        Roles Get
        Provides to get role
        ---
        tags:
          - role

        parameters:
          - in: path
            name: role_id
            type: string
            required: true

        responses:
          200:
            description: role data
            schema:
              properties:
                id:
                  type: UUID
                  description: id of role
                name:
                  type: string
                  description: name of role
                description:
                  type: string
                  description: description of role
          404:
            description: Role is not found
                """
        role_data = Role.find_by_id(id)
        if role_data:
            return role_schema.dump(role_data)
        return {'message': ROLE_NOT_FOUND}, 404

    def delete(self, id):
        """
        Roles Delete
        Provides to delete role
        ---
        tags:
          - role

        parameters:
          - in: path
            name: role_id
            type: string
            required: true

        responses:
          200:
            description: Role Deleted successfully
          404:
            description: Role is not found
         """
        role_data = Role.find_by_id(id)
        if role_data:
            role_data.delete_from_db()
            return {'message': "Role Deleted successfully"}, 200
        return {'message': ROLE_NOT_FOUND}, 404

    def put(self, id):
        """
        Roles update
        Provides to update role
        ---
        tags:
          - role

        parameters:
          - in: path
            name: role_id
            type: string
            required: true

        responses:
          200:
            description: role data
            schema:
              properties:
                id:
                  type: UUID
                  description: id of role
                name:
                  type: string
                  description: name of role
                description:
                  type: string
                  description: description of role
          404:
            description: Role is not found
         """
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
        """
        Get roles
        Provides to get all roles
        ---
        tags:
          - roles

        responses:
          200:
            description: all roles data
            schema:
              properties:
                id:
                  type: UUID
                  description: id of role
                name:
                  type: string
                  description: name of role
                description:
                  type: string
                  description: description of role
                 """
        return role_list_schema.dump(Role.find_all()), 200

    def post(self):
        """
        Create role
        Provides to create role
        ---
        tags:
          - roles

        responses:
          201:
            description: Role successfully created
            schema:
              properties:
                id:
                  type: UUID
                  description: id of role
                name:
                  type: string
                  description: name of role
                description:
                  type: string
                  description: description of role
          404:
            description: Role with same name already exists
          400:
            description: ValidationError
        """
        role_json = request.get_json()
        try:
            role_data = role_schema.load(role_json)
        except ValidationError as err:
            return {'message': err.messages}, 400
        if role_data.find_by_name(role_json['name']):
            return {'message': ROLE_NAME_AlREADY_EXISTS.format(role_json['name'])}, 404
        else:
            role_data.save_to_db()

        return role_schema.dump(role_data), 201
