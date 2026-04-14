import sys
import os

# Ensure the project root is in sys.path so 'src' can be imported correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sqlalchemy.sql import text
from src.db.database import engine

def check_db_identity():
    print("--- Checking Database Connection Identity ---")
    
    try:
        with engine.connect() as connection:
            # Query various connection parameters
            db_name = connection.execute(text("SELECT current_database();")).scalar()
            user = connection.execute(text("SELECT current_user;")).scalar()
            version = connection.execute(text("SELECT version();")).scalar()
            
            print(f"\n[SUCCESS] Connected to PostgreSQL!\n")
            print(f"Database Name : {db_name}")
            print(f"Database User : {user}")
            
            # Formatting the version string slightly so it fits nicely
            short_version = version.split()[1] if version else 'Unknown'
            print(f"Server Version: {short_version}")
            
            # Pulling a few public tables just as proof
            schemas_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                LIMIT 5;
            """)
            tables = connection.execute(schemas_query).fetchall()
            table_names = [t[0] for t in tables]
            
            if table_names:
                print(f"Public Tables : {', '.join(table_names)}")
            else:
                print("Public Tables : (No tables found in public schema yet)")
                
    except Exception as e:
        print("\n[ERROR] Connection failed:", e)

if __name__ == "__main__":
    check_db_identity()
