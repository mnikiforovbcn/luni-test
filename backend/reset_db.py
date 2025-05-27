import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from backend.db import DATABASE_URL, metadata, users

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    # Drop existing tables
    conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    
    # Create tables
    metadata.create_all(engine)
    print("Database tables have been reset")
