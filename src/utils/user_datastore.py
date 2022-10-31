from flask_security import SQLAlchemyUserDatastore

from src.db.db_postgres import db
from src.models.users import User
from src.models.roles import Role


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
