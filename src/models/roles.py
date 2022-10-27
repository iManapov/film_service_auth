import uuid

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import UUID
from src.db.db_postgres import db

from flask_security import RoleMixin


class Role(db.Model, RoleMixin):
    __tableName__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    __table_args__ = (
        Index('role_name_index', name),  # composite index on name
    )

    def __repr__(self):
        return f'<Role {self.name}>'
