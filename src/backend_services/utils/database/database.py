from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool
from typing import Generator

from utils.schemas import DatabaseSettings, DatabaseURL


def get_database_url(url: DatabaseURL):
    return f"postgresql+psycopg2://{url.username}:{url.password}@{url.host}:{url.port}/{url.db_name}"


def db_connection(url: DatabaseURL, settings: DatabaseSettings) -> sessionmaker:
    engine = create_engine(
        get_database_url(url),
        poolclass=QueuePool,
        pool_pre_ping=settings.pool_pre_ping,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        pool_recycle=settings.pool_recycle,
    )

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db(session_factory: sessionmaker) -> Generator[Session, None, None]:
    db: Session = session_factory()

    try:
        yield db

    finally:
        db.close()
