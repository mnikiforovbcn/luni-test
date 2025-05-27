import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text

try:
    # Connect as postgres user
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="Nextret2025",
        database="luni"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR NOT NULL UNIQUE,
            age INTEGER,
            gender VARCHAR,
            tg_user_id VARCHAR,
            tg_username VARCHAR
        )
    """)

    print("Tables created successfully")

    # Grant permissions to luni user
    cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO luni")
    cursor.execute("GRANT USAGE ON SCHEMA public TO luni")
    cursor.execute("GRANT ALL PRIVILEGES ON DATABASE luni TO luni")
    
    print("Permissions granted successfully!")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
