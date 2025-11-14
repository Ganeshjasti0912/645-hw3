from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# Create database URL for SQLModel
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Dependency to get DB session
def get_session():
    with Session(engine) as session:
        yield session
