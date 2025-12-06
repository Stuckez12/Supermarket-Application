from abc import abstractmethod
from sqlalchemy import Table
from sqlalchemy.orm import Session
from typing import Self, TypeVar
from uuid import UUID

from account.models.model_base import Base


ModelRow = TypeVar("ModelRow", bound=Base)


class BaseDBService:
    def __init__(self: Self, db: Session):
        self.db = db

    @property
    @abstractmethod
    def table(self: Self) -> Table:
        pass

    def get_by_id(self: Self, id: UUID):
        return self.db.query(self.table).filter(self.table.id == id).first()

    def get_paginated(self: Self, page: int, page_size: int):
        offset = (page - 1) * page_size
        return self.db.query(self.table).limit(page_size).offset(offset)

    def get_all(self: Self):
        return self.db.query(self.table).all()

    def add(self: Self, row: ModelRow):
        self.db.add(row)
        self.db.flush()

    def add_all(self: Self, rows: list[ModelRow]):
        self.db.add_all(rows)
        self.db.flush()

    def delete(self: Self, row: ModelRow):
        self.db.delete(row)

    def bulk_delete(self: Self, rows: list[ModelRow]):
        for row in rows:
            self.delete(row)
