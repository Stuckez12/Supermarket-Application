from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from utils.schemas import DatabaseSettings, DatabaseURL


Base = declarative_base()


def db_connection(url: DatabaseURL, settings: DatabaseSettings) -> sessionmaker:
    # Create engine
    engine = create_engine(
        f"postgresql+psycopg2://{url.username}:{url.password}@{url.host}:{url.port}/{url.db_name}",
        poolclass=QueuePool,
        pool_pre_ping=settings.pool_pre_ping,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        pool_recycle=settings.pool_recycle,
    )

    # Return session factory
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db(session_factory: sessionmaker):
    db = session_factory()

    try:
        yield db

    finally:
        db.close()
