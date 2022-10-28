from src.extensions import ma
from src.models.users import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        load_only = ("users",)
        # include_fk= True
