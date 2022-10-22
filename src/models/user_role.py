
import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from src.db.db_postgres import db


class UserRole(db.Model):
    __tableName__ = 'user_role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'), nullable=False)
    roles = db.relationship("roles", lazy="dynamic", primaryjoin="Roles.id == UserRole.role_id")
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    users = db.relationship("users", lazy="dynamic", primaryjoin="Users.id == UserRole.user_id")

    def __repr__(self):
        return f'<User {self.login}>'
