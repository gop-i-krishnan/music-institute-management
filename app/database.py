from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection URL for the music institute database.
# PostgreSQL connection URL loaded securely from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine manages the database connection pool.
engine = create_engine(DATABASE_URL)

# Session factory used by routes and services for database work.
SessionLocal = sessionmaker(bind=engine)

# Base class used by all SQLAlchemy model classes.
Base = declarative_base()


# Dependency that provides a database session and closes it after the request.
def get_db():
    # Each request gets its own session instance.
    db = SessionLocal()
    try:
        yield db
    finally:
        # Always close the session, even if the route raises an error.
        db.close()
