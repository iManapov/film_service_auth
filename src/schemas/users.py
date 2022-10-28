from src.core.ma import ma
from src.models.users import Users


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        load_only = ("users",)
        # include_fk= True
from src.core.ma import ma
from src.models.users import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        load_only = ("users",)