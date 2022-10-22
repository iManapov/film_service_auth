import uuid

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.db_postgres import db


class Users(db.Model):
    __tableName__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'), nullable=False)
    roles = relationship("user_role", lazy="dynamic", primaryjoin="user_role.role_id == Users.role_id")

    __table_args__ = (
        Index('users_login_index', login),  # composite index on login
    )

    def __repr__(self):
        return f'<Users {self.login}>'


#
#
# class BookSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Book
#         include_fk = True