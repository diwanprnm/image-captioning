from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

# Engine dibuat di sini, tapi tabel dibuat di Task 5 (startup event)
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=False)


def create_db_and_tables():
    """Create all tables. Called on startup (Task 5)."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency: yields a DB session."""
    with Session(engine) as session:
        yield session