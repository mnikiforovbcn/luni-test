import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncpg
from .db import DATABASE_URL

async def main():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Drop existing tables if they exist
        await conn.execute("DROP TABLE IF EXISTS users CASCADE")
        await conn.execute("DROP TABLE IF EXISTS messages CASCADE")
        
        # Create tables
        await conn.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                age INTEGER,
                gender VARCHAR(50),
                tg_user_id VARCHAR(255),
                tg_username VARCHAR(255)
            )
        """)
        
        await conn.execute("""
            CREATE TABLE messages (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                tg_user_id VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP NOT NULL
            )
        """)
        
        print("Database reset completed successfully")
    except Exception as e:
        print(f"Error resetting database: {str(e)}")
    finally:
        await conn.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
