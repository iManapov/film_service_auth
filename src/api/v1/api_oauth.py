
from flask import redirect, url_for, flash
from flask_restful import Resource
from flask_login import current_user

from src.api.v1.oauth import OAuthSignIn
from src.db.db_postgres import db
from src.models.social_accounts import SocialAccount
from src.models.users import User
from src.schemas.social_accounts import SocialAccountSchema
from src.utils.security import get_hash, generate_random_string
from src.utils.tokens import create_and_output_tokens
from src.utils.user_datastore import user_datastore

social_account_schema = SocialAccountSchema()


class Authorize(Resource):
    def get(self, provider):
        """
        Endpoint of the Authorize with chosen provider
        ---
        tags:
          - oauth

        parameters:
          - in: path
            name: provider
            type: string
            required: true
        """
        if not current_user.is_anonymous:
            return redirect(url_for('api_v1.login'))
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.authorize()


class Callback(Resource):
    def get(self, provider):
        """
        Endpoint of the Callback who get data from chosen provider
        ---
        tags:
          - oauth

        parameters:
          - in: path
            name: provider
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
                user_id:
                    type: string
                    description: user_id
        """
        if not current_user.is_anonymous:
            return redirect(url_for('api_v1.login'))
        oauth = OAuthSignIn.get_provider(provider)
        # Получение данных от поставщика
        social_id, social_name, username, email, first_name, last_name, user_agent = oauth.callback()
        if social_id is None:
            flash('Authentication failed.')
            return redirect(url_for('api_v1.login'))
        # Поиск в базе по фильтру
        soc_acc = SocialAccount.get_by_social_id_and_social_name(str(social_id), social_name)
        if not soc_acc:
            user = User.get_user_by_universal_login(username, email)
            if not user:
                data = {
                    "email": email,
                    "login": username,
                    "first_name": first_name or "first_name",
                    "last_name": last_name or "last_name"
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

        user = User.get_by_id(soc_acc.user_id)
        return create_and_output_tokens(user, user_agent)
