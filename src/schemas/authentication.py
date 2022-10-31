from src.extensions import ma
from src.models.authentication import Authentication


class AuthSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Authentication
        load_instance = True
        load_only = ("authentication",)
