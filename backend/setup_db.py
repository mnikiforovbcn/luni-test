import psycopg2

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
    # Drop existing table if it exists
    cursor.execute("DROP TABLE IF EXISTS users CASCADE")
    
    # Create table with proper sequence
    cursor.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            age INTEGER,
            gender VARCHAR(50),
            tg_user_id VARCHAR(255),
            tg_username VARCHAR(255)
        )
    """)
    
    # Grant permissions to luni user
    cursor.execute("GRANT ALL PRIVILEGES ON TABLE users TO luni")
    cursor.execute("GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO luni")
    
    print("Database setup completed successfully")
except Exception as e:
    print(f"Error setting up database: {e}")
finally:
    cursor.close()
    conn.close()
