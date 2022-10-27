import uuid

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from src.db.db_postgres import db


class UserRole(db.Model):
    __tableName__ = 'user_role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), ForeignKey('role.id'), nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'
