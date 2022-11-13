from http import HTTPStatus

from flask import redirect, url_for, flash, jsonify
from flask_restful import Resource
from flask_login import current_user
from requests import post

from src.api.v1.oauth import OAuthSignIn
from src.db.db_postgres import db
from src.models.social_accounts import SocialAccount
from src.models.users import User
from src.schemas.social_accounts import SocialAccountSchema
from src.utils.security import get_hash, generate_random_string
from src.utils.user_datastore import user_datastore

social_account_schema = SocialAccountSchema()


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))


class Authorize(Resource):
    def get(self, provider):
        """
        Roles Get
        Provides to get role
        ---
        tags:
          - roles

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
        # role_data = Role.find_by_id(id)
        # if role_data:
        #     return role_schema.dump(role_data)
        # return {"message": ROLE_NOT_FOUND}, HTTPStatus.NOT_FOUND
        if not current_user.is_anonymous:
            return redirect(url_for('api_v1.login'))
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.authorize()


class Callback(Resource):
    def get(self, provider):
        if not current_user.is_anonymous:
            return redirect(url_for('api_v1.login'))
        oauth = OAuthSignIn.get_provider(provider)
        social_id, social_name, username, email, first_name, last_name = oauth.callback()
        if social_id is None:
            flash('Authentication failed.')
            return redirect(url_for('api_v1.login'))
        soc_acc = SocialAccount.get_by_social_id_and_social_name(str(social_id), social_name)
        if not soc_acc:
            user = User.get_user_by_universal_login(username, email)
            if not user:
                data = {
                    "email": email,
                    "login": username,
                    "first_name": first_name or "first_name",
                    "last_name":  last_name or "last_name"
                }
                password = generate_random_string()
                hash_ = get_hash(password)
                data["password"] = hash_
                user = user_datastore.create_user(**data)
                db.session.commit()
            data_soc_acc = {
                "user_id": user.id,
                "social_id": str(social_id),
                "social_name": social_name
            }
            soc_acc = social_account_schema.load(data_soc_acc)
            soc_acc.save_to_db()
            return {"social_name": soc_acc.social_name, "user": user.login}, HTTPStatus.CREATED
        user = User.get_by_id(soc_acc.user_id)
        # Получить логин пароль и отправить на ручку логина
        # return redirect(url_for('api_v1.login', login=user.login,  password=user.password, methods=['POST']))
        # return jsonify(post("token", data).json())
        data = {
            "login": user.login,
            "password": str(user.password)
        }
        header = {'Content-Type': 'application/json'}
        return jsonify(post(url_for('api_v1.login', _external=True), json=data, headers=header).json())



