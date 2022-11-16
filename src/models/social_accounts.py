import uuid

from sqlalchemy import and_

from src.db.db_postgres import db
from sqlalchemy.dialects.postgresql import UUID


class SocialAccount(db.Model):
    __tablename__ = 'social_account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"))
    users = db.relationship("User", back_populates="social_accounts")
    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'),)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'

    @classmethod
    def get_by_social_id(cls, social_id) -> "SocialAccount":
        return cls.query.filter(cls.social_id == social_id).first()

    @classmethod
    def get_by_social_id_and_social_name(cls, social_id: str, social_name) -> "SocialAccount":
        """Return SocialAccount object after filter social_id == social_id and social_name == social_name"""
        return cls.query.filter(and_(cls.social_id == social_id, cls.social_name == social_name)).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

