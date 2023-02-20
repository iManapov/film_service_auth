from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.db.db_postgres import db


class AbstractORM(ABC):
    """
    Abstract db class
    """
    @abstractmethod
    def insert(self, row):
        pass

    @abstractmethod
    def delete(self, row):
        pass


@dataclass
class SQLAlchemy(AbstractORM):
    """
    SQL Alchemy db class
    """

    database: db = db

    def insert(self, row: db.Model):
        """
        Inserts row to db table

        :param row: row to insert
        """

        db.session.add(row)
        db.session.commit()

    def delete(self, row: db.Model):
        pass
