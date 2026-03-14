from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


def _get_database_url() -> str:
    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Create backend/.env and set DATABASE_URL, "
            'e.g. DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/global_vision"'
        )
    return settings.database_url


engine = create_engine(_get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

