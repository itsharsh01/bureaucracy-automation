import os
from sqlalchemy import create_engine, text
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


def apply_schema_updates() -> None:
    """Apply lightweight non-destructive schema updates for evolving models."""
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1
                        FROM pg_type t
                        JOIN pg_namespace n ON n.oid = t.typnamespace
                        WHERE t.typname = 'userrole' AND n.nspname = 'public'
                    ) THEN
                        ALTER TYPE public.userrole ADD VALUE IF NOT EXISTS 'operator';
                    END IF;
                END $$;
                """
            )
        )
        connection.execute(
            text(
                """
                ALTER TABLE IF EXISTS public.app_users
                ADD COLUMN IF NOT EXISTS department VARCHAR
                """
            )
        )
        connection.execute(
            text(
                """
                ALTER TABLE IF EXISTS public.app_users
                ADD COLUMN IF NOT EXISTS company_name VARCHAR
                """
            )
        )
        connection.execute(
            text(
                """
                ALTER TABLE IF EXISTS public.chatbot_queries
                ADD COLUMN IF NOT EXISTS customer_id INTEGER
                """
            )
        )
        connection.execute(
            text(
                """
                ALTER TABLE IF EXISTS public.chatbot_queries
                ADD COLUMN IF NOT EXISTS company_response TEXT
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS ix_chatbot_queries_customer_id
                ON public.chatbot_queries (customer_id)
                """
            )
        )

# Dependency for FastAPI to get DB sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()