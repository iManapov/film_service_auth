from src.extensions import ma
from src.models.roles import Role


class RoleSchema(ma.SQLAlchemySchema):

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()

    class Meta:
        model = Role
        load_instance = True
        load_only = ("roles",)
