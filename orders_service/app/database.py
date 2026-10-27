import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()


def read_secret(name: str) -> str:
    """Read a secret from the Docker secrets filesystem."""
    secret_path = Path(f"/run/secrets/{name}")
    if not secret_path.is_file():
        raise RuntimeError(f"Required secret file not found: {secret_path}")
    return secret_path.read_text(encoding="utf-8").strip()


user = os.getenv("POSTGRES_USER", "orders")
database = os.getenv("POSTGRES_DB", "orders")
host = os.getenv("POSTGRES_HOST", "postgres")
port = int(os.getenv("POSTGRES_PORT", "5432"))

password = read_secret("db_password")

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=user,
    password=password,
    host=host,
    port=port,
    database=database,
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


def get_db():
    """Provide a database session for a request."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()