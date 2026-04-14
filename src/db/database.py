import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

try:
    if not DATABASE_URL:
        raise ValueError("DB_URL is not set in the environment variables.")
    
    engine = create_engine(DATABASE_URL)
    
    # Test the connection to ensure the DB is reachable at startup
    with engine.connect() as connection:
        print("Successfully connected to the database!")
except Exception as e:
    print(f"Error initializing the database connection: {e}")
    import sys
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI to get DB sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()