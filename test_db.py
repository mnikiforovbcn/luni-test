import psycopg2
from psycopg2 import OperationalError

try:
    # Try to connect to the default PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="Nextret2025"  # Replace with your actual PostgreSQL password
    )
    print("Successfully connected to PostgreSQL!")
    conn.close()
except OperationalError as e:
    print(f"Error connecting to PostgreSQL: {e}")
