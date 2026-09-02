import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

database_url = settings.DATABASE_URL
if database_url.startswith("postgresql") and "+psycopg2" not in database_url and "+asyncpg" not in database_url:
    database_url = database_url.replace("postgresql://", "postgresql+psycopg2://")

def get_engine():
    try:
        # Test connecting to Postgres
        engine_test = create_engine(
            database_url,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 2},
        )
        with engine_test.connect():
            pass
        return engine_test
    except Exception as e:
        # Fallback to local SQLite development database if PostgreSQL is not reachable
        sqlite_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "smartserve_dev.db"))
        return create_engine(
            f"sqlite:///{sqlite_path}",
            connect_args={"check_same_thread": False},
        )

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
