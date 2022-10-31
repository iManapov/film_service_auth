import uuid

from sqlalchemy.dialects.postgresql import UUID

from src.db.db_postgres import db


roles_users = db.Table(
    'user_role',
    db.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.id')),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id'))
)
