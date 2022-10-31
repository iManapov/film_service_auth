import uuid
from typing import List

from sqlalchemy import Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from flask_security import RoleMixin

from src.db.db_postgres import db


class Role(db.Model, RoleMixin):
    __tableName__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    __table_args__ = (
        Index('role_name_index', name),  # composite index on name
    )

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return 'Roles(name=%s, description=%s)' % (self.name, self.description)

    def json(self):
        return {'name': self.name, 'description': self.description}

    @classmethod
    def find_by_name(cls, name) -> "Role":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "Role":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["Role"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
