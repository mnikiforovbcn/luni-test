import psycopg2
import os

# Connect as postgres user
conn = psycopg2.connect(
    dbname="luni",
    user="postgres",
    password="Nextret2025",  # Change this to your postgres password
    host="localhost",
    port=5432
)

# Enable autocommit
conn.autocommit = True

cursor = conn.cursor()

try:
    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS users CASCADE")
    cursor.execute("DROP TABLE IF EXISTS messages CASCADE")
    
    # Create tables
    cursor.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            age INTEGER,
            gender VARCHAR(50),
            tg_user_id VARCHAR(255),
            tg_username VARCHAR(255)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE messages (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            tg_user_id VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP NOT NULL
        )
    """)
    
    # Create sequences
    cursor.execute("CREATE SEQUENCE IF NOT EXISTS users_id_seq")
    cursor.execute("CREATE SEQUENCE IF NOT EXISTS messages_id_seq")
    
    # Grant permissions to luni user
    cursor.execute("GRANT ALL PRIVILEGES ON DATABASE luni TO luni")
    cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO luni")
    cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO luni")
    cursor.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO luni")
    cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO luni")
    cursor.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO luni")
    
    print("Database setup completed successfully")
except Exception as e:
    print(f"Error setting up database: {str(e)}")
finally:
    cursor.close()
    conn.close()
