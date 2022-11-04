import jwt
from datetime import timedelta
from http import HTTPStatus

from flask import jsonify
from flask_restful import Resource, request
from flask_security.utils import hash_password
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, get_jwt_identity, get_jti, get_jwt
from flasgger import swag_from

from sqlalchemy.exc import IntegrityError

from src.db.db_postgres import db
from src.db.db_redis import jwt_redis_blocklist, jwt_redis_refresh
from src.models.users import User
from src.models.authentication import Authentication
from src.models.roles import Role
from src.utils.db import SQLAlchemy
from src.utils.user_datastore import user_datastore
from src.utils.security import get_hash, check_password
from src.schemas.users import UserSchema
from src.utils.uuid_checker import is_uuid
from src.extensions import jwt


ACCESS_EXPIRES = timedelta(hours=1)
user_schema = UserSchema()
ACCESS_EXPIRES = timedelta(minutes=2)
REFRESH_EXPIRES = timedelta(minutes=2)

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


class SignUp(Resource):
    """
    API-view для регистрации пользователя
    """
    def post(self):
        """
        User signup
        Provides user signup
        ---
        tags:
          - users
        parameters:
          - in: body
            name: login
            type: string
            required: true
          - in: body
            name: password
            type: string
            required: true
          - in: body
            name: email
            type: string
            required: true
          - in: body
            name: first_name
            type: string
            required: false
          - in: body
            name: last_name
            type: string
            required: false
          - in: body
            name: roles
            description: list of role IDs
            type: array
            required: false
            items:
              type: string
        responses:
          201:
            description: A single user item
            schema:
              id: User
              properties:
                user:
                  type: string
                  description: The name of the user
          400:
            description: Invalid credentials
        """
        try:
            data = request.get_json()
            if (data.get("login") and data.get("password") and data.get("email")) is None:
                return {"error": "Credentials required: login, email and password"}, HTTPStatus.BAD_REQUEST
            hash_ = get_hash(data["password"])
            data["password"] = hash_
            user_datastore.create_user(**data)
            db.session.commit()
            return {"user": data["login"]}, HTTPStatus.CREATED
        except IntegrityError:
            return {"error": "Login or email already exist or missing required data"}, HTTPStatus.BAD_REQUEST


class Login(Resource):
    """
    API-view для получения access- и refresh-токенов
    при вводе логина и пароля
    """
    def post(self):
        """
        User login
        Provides to get access and refresh tokens
        ---
        tags:
          - users
        parameters:
          - in: body
            name: login
            type: string
            required: true
          - in: body
            name: password
            type: string
            required: true
        responses:
          200:
            description: access and refresh token
            schema:
              properties:
                access_token:
                  type: string
                  description: access_token
                refresh_token:
                  type: string
                  description: refresh_token
          400:
            description: Invalid credentials
          401:
            description: Credentials required
        """
        data = request.get_json()
        user_agent = str(request.user_agent)
        if not data:
            return {"error": "Credentials required"}, HTTPStatus.BAD_REQUEST
        user = user_datastore.find_user(login=data["login"])

        if user and check_password(data["password"], user.password):
            refresh_token = create_refresh_token(identity=user.id)
            auth_hist = Authentication(user_id=user.id, user_agent=user_agent)
            db.session.add(auth_hist)
            db.session.commit()
            # сохранять refresh-токен в базе
            jti_refresh = get_jti(refresh_token)
            additional_claims = {"jti_refresh": jti_refresh}
            access_token = create_access_token(identity=user.id,
                                               additional_claims=additional_claims)
            jwt_redis_refresh.set(get_jti(refresh_token), str(user.id), ex=REFRESH_EXPIRES)
            return {"access_token": access_token,
                    "refresh_token": refresh_token,
                    "user_id": str(user.id)}, HTTPStatus.OK
        return {"error": "Invalid credentials"}, HTTPStatus.BAD_REQUEST


class RefreshTokens(Resource):
    """
    API-view для получения новых access- и refresh-токенов
    с помощью refresh-токена
    """
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh tokens
        Provides to get new access and refresh tokens
        ---
        tags:
          - users
        parameters:
          - in: body
            name: refresh_token
            type: string
            required: true
        security:
          BearerAuth:
            type: http
            scheme: bearer
        responses:
          200:
            description: new access and refresh token
            schema:
              properties:
                access_token:
                  type: string
                  description: access_token
                refresh_token:
                  type: string
                  description: refresh_token
          400:
            description: Token is invalid
        """
        jti = get_jwt()["jti"]
        identity = get_jwt_identity()

        if jwt_redis_refresh.get(jti) == identity:
            jwt_redis_refresh.delete(jti)

            refresh_token = create_refresh_token(identity=identity)
            jti_refresh = get_jti(refresh_token)
            additional_claims = {"jti_refresh": jti_refresh}
            access_token = create_access_token(identity=identity,
                                               fresh=False,
                                               additional_claims=additional_claims)

            jwt_redis_refresh.set(jti_refresh, identity, ex=REFRESH_EXPIRES)
        else:
            return {"error": "Token is invalid"}, HTTPStatus.BAD_REQUEST
        return {"access_token": access_token, "refresh_token": refresh_token}, HTTPStatus.OK


class Logout(Resource):
    """
    API-view для выхода пользователя из системы
    и помещения его access-токена в блок-лист
    """
    @jwt_required(verify_type=False)
    def delete(self):
        """
        User logout
        Provides user logout
        ---
        tags:
          - users
        parameters:
          - in: body
            name: access_token
            type: string
            required: true
        security:
          BearerAuth:
            type: http
            scheme: bearer
        responses:
          201:
            description: A single user item
            schema:
              id: User
              properties:
                user:
                  type: string
                  description: The name of the user
          422:
            description: Invalid token
        """
        token = get_jwt()
        jti = token["jti"]

        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        refresh_jti = token["jti_refresh"]
        jwt_redis_refresh.delete(refresh_jti)

        return {"msg": "User's token revoked"}, HTTPStatus.OK


class ChangeCreds(Resource):
    """API-view для изменения данных пользователя."""

    @jwt_required()
    def put(self, user_id):
        """
        Update user credentials
        Updates user credentials
        ---
        tags:
          - users
        parameters:
          - name: user_id
            in: path
            type: uuid
            required: true
            default: all
          - in: body
            name: login
            type: string
            required: false
          - in: body
            name: password
            type: string
            required: false
          - in: body
            name: email
            type: string
            required: false
          - in: body
            name: first_name
            type: string
            required: false
          - in: body
            name: last_name
            type: string
            required: false
        security:
          BearerAuth:
            type: http
            scheme: bearer
        responses:
          200:
            description: User credentials updated
            schema:
              properties:
                msg:
                  type: string
                  description: User updated
                result:
                  type: object
                  description: Updated user info
          400:
            description: Token is invalid
        """

        if not is_uuid(user_id):
            return {"error": "Invalid UUID format"}, HTTPStatus.BAD_REQUEST
        try:
            data = request.get_json()
            if not data:
                return {"msg": "Empty data"}, HTTPStatus.BAD_REQUEST
            user = User.get_by_id(user_id)
            if not user:
                return {"error": "No user with specified id"}, HTTPStatus.BAD_REQUEST
            for key, value in data.items():
                if key == "password":
                    hash_ = get_hash(data["password"])
                    value = hash_
                setattr(user, key, value)
            db.session.commit()
            return {"msg": "User updated", "result": user_schema.dump(user)}, HTTPStatus.OK
        except IntegrityError:
            return {"error": "Login or email already exist"}, HTTPStatus.BAD_REQUEST


class LoginHistory(Resource):
    """API-view для просмотра истории входов."""

    @jwt_required()
    def get(self, user_id):
        """
        Get user login history
        Get user login history
        ---
        tags:
          - users
        parameters:
          - name: user_id
            in: path
            type: uuid
            required: true
          - name: page
            in: query
            type: int
            required: False
            default: 1
          - name: size
            in: query
            type: int
            required: False
            default: 20
        security:
          BearerAuth:
            type: http
            scheme: bearer
        responses:
          200:
            description: User login history
            schema:
              properties:
                result:
                  type: array
                  items:
                    type: object
                  description: User login history
          400:
            description: Invalid uuid
        """
        if not is_uuid(user_id):
            return {"error": "Invalid UUID format"}, HTTPStatus.BAD_REQUEST
        try:
            page = int(request.args.get("page", 1))
            size = int(request.args.get("size", 20))
        except ValueError:
            return {"error": "Page and size query parameters must be integer"}, HTTPStatus.BAD_REQUEST
        history = Authentication.get_login_history(user_id, page=page, size=size)
        return {"result": [x.as_dict() for x in history]}, HTTPStatus.OK


class UserRoles(Resource):
    """API-view для просмотра ролей пользователя."""

    @jwt_required()
    def get(self, user_id):
        """
        Get users roles
        Get users roles
        ---
        tags:
          - users
        parameters:
          - name: user_id
            in: path
            type: uuid
            required: true
            default: all
        security:
          BearerAuth:
            type: http
            scheme: bearer
        responses:
          200:
            description: Users roles
            schema:
              properties:
                result:
                  type: array
                  items:
                    type: object
                  description: Users roles
          400:
            description: Invalid uuid
        """

        if not is_uuid(user_id):
            return {"error": "Invalid UUID format"}, HTTPStatus.BAD_REQUEST
        user = User.get_by_id(user_id)
        if not user:
            return {"error": "No user with specified id"}, HTTPStatus.BAD_REQUEST
        return {"result": [x.json() for x in user.roles]}, HTTPStatus.OK


class ChangeUserRoles(Resource):
    """API-view для изменения ролей пользователя."""

    @jwt_required()
    def post(self, user_id, role_id):
        """
        Add role to user
        Adds role <role_id> to user <user_id>
        ---
        tags:
          - users
        parameters:
          - name: user_id
            in: path
            type: uuid
            required: true
            default: all
          - name: role_id
            in: path
            type: uuid
            required: true
            default: all
        security:
          BearerAuth:
            type: http
            scheme: bearer
        responses:
          200:
            description: User role added
            schema:
              properties:
                msg:
                  type: string
                  description: Role added
          400:
            description: Invalid uuid format
        """

        if not (is_uuid(user_id) and is_uuid(role_id)):
            return {"error": "Invalid UUID format"}, HTTPStatus.BAD_REQUEST
        user = User.get_by_id(user_id)
        if not user:
            return {"error": "No user with specified id"}, HTTPStatus.BAD_REQUEST
        role = Role.find_by_id(role_id)
        if not role:
            return {"error": "No role with specified id"}, HTTPStatus.BAD_REQUEST
        user_datastore.add_role_to_user(user, role)
        db.session.commit()
        return {"msg": "Success"}, HTTPStatus.OK

    @jwt_required()
    def delete(self, user_id, role_id):
        """
        Delete role from user
        Delete role <role_id> from user <user_id>
        ---
        tags:
          - users
        parameters:
          - name: user_id
            in: path
            type: uuid
            required: true
            default: all
          - name: role_id
            in: path
            type: uuid
            required: true
            default: all
        security:
          BearerAuth:
            type: http
            scheme: bearer
        responses:
          200:
            description: User role deleted
            schema:
              properties:
                msg:
                  type: string
                  description: Role deleted
          400:
            description: Invalid uuid format
        """

        if not (is_uuid(user_id) and is_uuid(role_id)):
            return {"error": "Invalid UUID format"}, HTTPStatus.BAD_REQUEST
        user = User.get_by_id(user_id)
        if not user:
            return {"error": "No user with specified id"}, HTTPStatus.BAD_REQUEST
        role = Role.find_by_id(role_id)
        if not role:
            return {"error": "No role with specified id"}, HTTPStatus.BAD_REQUEST
        user_datastore.remove_role_from_user(user, role)
        db.session.commit()
        return {"msg": "Success"}, HTTPStatus.OK
