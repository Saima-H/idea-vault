from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PASTE YOUR SUPABASE URL HERE
SQLALCHEMY_DATABASE_URL = "postgresql://postgres.kcphopjpvtrllckyjnfd:mypassword@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
