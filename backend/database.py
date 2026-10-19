from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This creates a file called vault.db in your backend folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./vault.db"

# The engine is the actual connection to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is what we use to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is what we use to define our tables
Base = declarative_base()