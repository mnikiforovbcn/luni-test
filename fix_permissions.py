import psycopg2

try:
    # Connect as postgres user
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="Nextret2025"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Grant permissions to luni user
    cursor.execute("GRANT ALL PRIVILEGES ON DATABASE luni TO luni")
    cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO luni")
    cursor.execute("GRANT USAGE ON SCHEMA public TO luni")
    cursor.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO luni")
    
    print("Permissions granted successfully!")
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
