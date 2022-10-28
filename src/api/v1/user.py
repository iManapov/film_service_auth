from datetime import timedelta

from flask_restful import Resource, request
from flask_security.utils import hash_password
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, get_jwt_identity
from flasgger import swag_from

from sqlalchemy.exc import IntegrityError

from src.db.db_postgres import db
from src.db.db_redis import jwt_redis_blocklist
from src.models.users import User
from src.utils.db import SQLAlchemy
from src.utils.user_datastore import user_datastore
from src.utils.security import get_hash, check_password


ACCESS_EXPIRES = timedelta(hours=1)


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
            if not data:
                return {'error': 'Credentials required'}, 400
            hash_ = get_hash(data["password"])
            data['password'] = hash_
            user_datastore.create_user(**data)
            db.session.commit()
            return {'user': data['login']}, 201
        except IntegrityError:
            return {'error': 'Login or email already exist'}, 400


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
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            # сохранять refresh-токен в базе
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        return {'error': 'Invalid credentials'}, 401


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
        try:
            identity = get_jwt_identity()
            access_token = create_access_token(identity=identity, fresh=False)
            refresh_token = create_refresh_token(identity=identity)
            # поместить старый refresh-токен в блок-лист
            # сохранять новый refresh-токен в базе
            # поместить старый access-токен в блок-лист
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        except jwt.exceptions.DecodeError: #, InvalidSignatureError):
            return {'error': 'Token is invalid'}, 401


class Logout(Resource):
    """
    API-view для выхода пользователя из системы
    и помещения его access-токена в блок-лист
    """
    @jwt_required
    def delete(self):
        jti = get_jwt()["jti"]
        jwt_redis_blocklistset(jti, "", ex=ACCESS_EXPIRES)
        # поместить старый access-токен в блок-лист
        # поместить старый refresh-токен в блок-лист
        return {"msg": "User's token revoked"}, 200
