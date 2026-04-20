import os
import sys

# Add the project root to sys.path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from src.db.database import engine

def alter_table():
    try:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE public.auth_users ADD COLUMN name VARCHAR;"))
        print("Successfully added 'name' column to 'auth_users' table.")
    except Exception as e:
        print(f"Error adding column (it might already exist): {e}")

if __name__ == "__main__":
    alter_table()
