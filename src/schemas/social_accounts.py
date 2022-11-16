from src.extensions import ma
from src.models.social_accounts import SocialAccount


class SocialAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SocialAccount
        load_instance = True
        load_only = ("social_account",)
        fields = ("id", "user_id", "social_id", "social_name")
