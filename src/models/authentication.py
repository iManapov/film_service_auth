import uuid

from sqlalchemy import ForeignKeyConstraint, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from src.db.db_postgres import db


class Authentication(db.Model):
    __tableName__ = 'authentication'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user_agent = db.Column(db.String, nullable=True)
    datetime = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        Index('authentication_user_id_index', user_id),  # composite index on user_id
    )

    @classmethod
    def get_login_history(cls, user_id, page, size):
        return cls.query.filter_by(user_id=user_id).order_by(cls.datetime.desc()).paginate(page=page, per_page=size)

    def as_dict(self) -> dict:
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
