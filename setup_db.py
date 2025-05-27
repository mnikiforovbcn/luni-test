import psycopg2
from psycopg2 import sql

try:
    # Connect to PostgreSQL as admin
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="Nextret2025"
    )
    conn.autocommit = True  # Needed for creating databases
    cursor = conn.cursor()

    # Create database
    cursor.execute(sql.SQL("CREATE DATABASE luni"))
    print("Database 'luni' created successfully")

    # Create user
    cursor.execute(sql.SQL("CREATE USER luni WITH PASSWORD 'luni'"))
    print("User 'luni' created successfully")

    # Grant permissions
    cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE luni TO luni"))
    cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON SCHEMA public TO luni"))
    print("Permissions granted to user 'luni'")

    cursor.close()
    conn.close()
    print("Database setup completed successfully!")

except Exception as e:
    print(f"Error: {e}")
