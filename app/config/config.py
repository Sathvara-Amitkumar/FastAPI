from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql+psycopg2://postrges:123@localhost:2580/project_fastapi"
engine = create_engine(db_url)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)