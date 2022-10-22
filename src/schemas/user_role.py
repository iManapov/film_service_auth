from src.core.ma import ma
from src.models.user_role import UserRole


class UserRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserRole
        load_instance = True
        load_only = ("user_role",)
        # include_fk= True