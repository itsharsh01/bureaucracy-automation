import sys
import os

# Ensure the project root is in sys.path so 'src' can be imported correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

# Import the engine and SessionLocal from database.py
from src.db.database import engine, SessionLocal

Base = declarative_base()

class DummyModel(Base):
    __tablename__ = "dummy_test_table"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    test = Column(String)
    test2 = Column(String)

def test_database_operations():
    print("--- Starting Database Test ---")
    
    try:
        # Create the table in the database
        print("1. Creating 'dummy_test_table'...")
        Base.metadata.create_all(bind=engine)
        print("   Table created successfully.")
        
        db = SessionLocal()
        
        # Insert a new record
        print("\n2. Inserting a record...")
        new_entry = DummyModel(name="Test Entry 1", description="Validating insert operations")
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        print(f"   Record inserted successfully with ID: {new_entry.id}")
        
        # Query the record back
        print("\n3. Querying the record...")
        queried = db.query(DummyModel).filter(DummyModel.id == new_entry.id).first()
        if queried:
            print(f"   Record retrieved successfully: '{queried.name}' - '{queried.description}'")
        else:
            print("   Failed to retrieve the record.")
            
    except Exception as e:
        print("\n[ERROR] Database operation failed:", e)
        if 'db' in locals():
            db.rollback()
    finally:
        if 'db' in locals():
            db.close()
        
        # Cleanup: Drop the test table so it doesn't pollute your database
        # print("\n4. Cleaning up (dropping test table)...")
        # Base.metadata.drop_all(bind=engine)
        # print("\n4. Table was NOT dropped so you can verify it in check_connection.py.")
        print("--- Test Complete ---")

if __name__ == "__main__":
    test_database_operations()
