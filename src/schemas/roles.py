from src.core.ma import ma
from src.models.roles import Roles


class RolesSchema(ma.SQLAlchemySchema):

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    class Meta:
        model = Roles
        load_instance = True
        load_only = ("roles",)
        # include_fk= True