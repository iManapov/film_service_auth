from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from src.db.db_postgres import db

# скорее всего убрать


class AbstractORM(ABC):
    """
    Абстрактный класс для работы с БД
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
    Класс для работы с БД через SQL Alchemy
    """
    database: db = db

    def insert(self, row: db.Model):
        """
        Метод для вставки записи в таблицу

        @param row: вставляемая запись
        """
        db.session.add(row)
        db.session.commit()

    def delete(self, row: db.Model):
        pass
