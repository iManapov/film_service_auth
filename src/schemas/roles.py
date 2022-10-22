from src.core.ma import ma
from src.models.roles import Roles


class RolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True
        load_only = ("roles",)
        # include_fk= True