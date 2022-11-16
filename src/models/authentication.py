import uuid

from sqlalchemy import event, ForeignKey, DDL, UniqueConstraint

from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from src.db.db_postgres import db
from sqlalchemy.ext.declarative import declared_attr


class AuthenticationMixin:
    @declared_attr
    def user_id(self):
        return db.Column(
            UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
        )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,  nullable=False)
    user_agent = db.Column(db.String, nullable=True)
    login_at = db.Column(db.DateTime, default=datetime.now, primary_key=True)

    def __repr__(self) -> str:
        return f"<Login history {self.id}>"

    def as_value(self) -> str:
        return self.event_type.value


class Authentication(AuthenticationMixin, db.Model):
    __tableName__ = "authentication"
    __table_args__ = (
        UniqueConstraint("login_at", "id"),
        {'postgresql_partition_by': 'RANGE (login_at)'},
    )

    @classmethod
    def get_login_history(cls, user_id, page, size):
        return cls.query.filter_by(user_id=user_id).order_by(cls.login_at.desc()).paginate(page=page, per_page=size)

    def as_dict(self) -> dict:
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Authentication2020(AuthenticationMixin, db.Model):
    __tablename__ = 'authentication2020'


class Authentication2021(AuthenticationMixin, db.Model):
    __tablename__ = 'authentication2021'


class Authentication2022(AuthenticationMixin, db.Model):
    __tablename__ = 'authentication2022'


class Authentication2023(AuthenticationMixin, db.Model):
    __tablename__ = 'authentication2023'


class Authentication2024(AuthenticationMixin, db.Model):
    __tablename__ = 'authentication2024'


PARTITION_TABLES_REGISTRY = (
    (Authentication2020, "('2020-01-01') TO ('2021-01-01')"),
    (Authentication2021, "('2021-01-01') TO ('2022-01-01')"),
    (Authentication2022, "('2022-01-01') TO ('2023-01-01')"),
    (Authentication2023, "('2023-01-01') TO ('2024-01-01')"),
    (Authentication2024, "('2024-01-01') TO ('2025-01-01')")
)


def create_table_login_history_partition_ddl(
    table: str, periods: str
) -> None:
    return DDL(
        """
        ALTER TABLE authentication ATTACH PARTITION %s FOR VALUES FROM %s;"""
        % (table, periods)
    ).execute_if(dialect="postgresql")


def attach_event_listeners() -> None:
    for class_, periods in PARTITION_TABLES_REGISTRY:
        class_.__table__.add_is_dependent_on(Authentication.__table__)
        event.listen(
            class_.__table__,
            "after_create",
            create_table_login_history_partition_ddl(
                class_.__table__, periods
            ),
        )


attach_event_listeners()
