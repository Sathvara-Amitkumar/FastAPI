import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# Render gives postgres:// or postgresql://
# SQLAlchemy + psycopg2 should use postgresql+psycopg2://
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://",1)

elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(db_url)

session = sessionmaker(bind=engine, autoflush=False, autocommit=False)