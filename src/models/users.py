import uuid
from datetime import datetime

from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flask_security import UserMixin

from src.db.db_postgres import db
from src.models.user_role import roles_users


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime(), default=datetime.now)
    is_administrator = db.Column(db.Boolean(), default=False)

    __table_args__ = (
        Index("users_login_index", login),  # composite index on login
    )

    @classmethod
    def get_by_id(cls, _id) -> "User":
        return cls.query.get(_id)

    def as_dict(self) -> dict:
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
