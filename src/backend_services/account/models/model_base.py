import uuid

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Self, cast


Base = declarative_base()


class BaseModel(Base):  # type: ignore
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
        primary_key=True,
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self: Self) -> str:
        cols = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return f"{self.__class__.__name__}({cols})"
