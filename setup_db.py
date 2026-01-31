"""
Database setup script for GutSense
Run this script to create the database and tables
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from app.database import Base
from app.config import settings
import sys


def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Parse database URL to get connection details
        db_url_parts = settings.DATABASE_URL.replace("postgresql://", "").split("/")
        db_name = db_url_parts[-1]
        connection_string = "/".join(db_url_parts[:-1])
        
        # Connect to PostgreSQL server (not specific database)
        conn = psycopg2.connect(f"postgresql://{connection_string}/postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"✅ Database '{db_name}' created successfully")
        else:
            print(f"ℹ️  Database '{db_name}' already exists")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        print("Make sure PostgreSQL is running and credentials are correct")
        sys.exit(1)


def create_tables():
    """Create all tables"""
    try:
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)


def main():
    """Main setup function"""
    print("🚀 Setting up GutSense database...")
    
    # Create database
    create_database()
    
    # Create tables
    create_tables()
    
    print("🎉 Database setup completed!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Start the server: python main.py")
    print("3. Visit: http://localhost:8000/docs for API documentation")


if __name__ == "__main__":
    main()