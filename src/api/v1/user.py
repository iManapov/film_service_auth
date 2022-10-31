import jwt
from datetime import timedelta

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
from src.utils.db import SQLAlchemy
from src.utils.user_datastore import user_datastore
from src.utils.security import get_hash, check_password
from src.extensions import jwt


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
                return {'error': 'Credentials required: login, email and password'}, 400
            hash_ = get_hash(data["password"])
            data['password'] = hash_
            user_datastore.create_user(**data)
            db.session.commit()
            return {'user': data['login']}, 201
        except IntegrityError:
            return {'error': 'Login or email already exist or missing required data'}, 400


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
        if not data:
            return {'error': 'Credentials required'}, 400
        user = user_datastore.find_user(login=data['login'])

        if user and check_password(data['password'], user.password):
            refresh_token = create_refresh_token(identity=user.id)
            jti_refresh = get_jti(refresh_token)
            additional_claims = {"jti_refresh": jti_refresh}
            access_token = create_access_token(identity=user.id,
                                               additional_claims=additional_claims)
            jwt_redis_refresh.set(get_jti(refresh_token), str(user.id), ex=REFRESH_EXPIRES)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        return {'error': 'Invalid credentials'}, 400


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
            return {'error': 'Token is invalid'}, 400
        return {'access_token': access_token, 'refresh_token': refresh_token}, 200


class Logout(Resource):
    """
    API-view для выхода пользователя из системы
    и помещения его access-токена в блок-лист
    """
    @jwt_required(verify_type=False)
    def delete(self):
        token = get_jwt()
        jti = token["jti"]

        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        refresh_jti = token["jti_refresh"]
        jwt_redis_refresh.delete(refresh_jti)

        return {"msg": "User's token revoked"}, 200
