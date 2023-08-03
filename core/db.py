from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()
engine = create_engine(os.environ.get("DATABASE_URL"))
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = session()
    try:
        yield db
        db.commit()
    finally:
        db.close()
