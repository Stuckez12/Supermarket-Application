import uuid

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, UUID

from utils.database.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
        primary_key=True,
        unique=True,
    )
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
