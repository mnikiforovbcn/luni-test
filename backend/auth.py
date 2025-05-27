from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from .db import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine
import asyncpg
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class UserIn(BaseModel):
    tg_user_id: str
    username: str | None = None
    age: int | None = None
    gender: str | None = None
    tg_username: str | None = None

class MessageIn(BaseModel):
    username: str
    message: str
    tg_user_id: str



@router.post("/register")
async def register(user: UserIn):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Check if username exists
        result = await conn.fetchrow("SELECT username FROM users WHERE username = $1", user.username)
        if result:
            raise HTTPException(status_code=400, detail="Username taken")
        
        # Insert new user
        await conn.execute("""
            INSERT INTO users (username, age, gender, tg_user_id, tg_username)
            VALUES ($1, $2, $3, $4, $5)
        """, user.username, user.age, user.gender, user.tg_user_id, user.tg_username)
        
        return {"msg": "Registered"}
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await conn.close()

@router.post("/check_user")
async def check_user(request: Request):
    data = await request.json()
    tg_user_id = data.get("tg_user_id")
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        result = await conn.fetchrow("SELECT username FROM users WHERE tg_user_id = $1", tg_user_id)
        if result:
            return {"exists": True, "username": result['username']}
        return {"exists": False}
    finally:
        await conn.close()

@router.post("/login")
async def login(user: UserIn):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        result = await conn.fetchrow("SELECT * FROM users WHERE tg_user_id = $1", user.tg_user_id)
        if not result:
            raise HTTPException(status_code=400, detail="User not found")
        
        # Update user info if any fields were provided
        update_data = {}
        if user.username is not None:
            update_data['username'] = user.username
        if user.age is not None:
            update_data['age'] = user.age
        if user.gender is not None:
            update_data['gender'] = user.gender
        if user.tg_username is not None:
            update_data['tg_username'] = user.tg_username
        
        if update_data:
            update_query = "UPDATE users SET " + ", ".join(f"{key} = ${i+1}" for i, key in enumerate(update_data.keys())) + " WHERE tg_user_id = $" + str(len(update_data.keys()) + 1)
            await conn.execute(update_query, *update_data.values(), user.tg_user_id)
        
        return {"msg": "Logged in", "username": result['username']}
    finally:
        await conn.close()

@router.post("/save_message")
async def save_message(message: MessageIn):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Verify user exists
        user_result = await conn.fetchrow("SELECT username FROM users WHERE tg_user_id = $1", message.tg_user_id)
        if not user_result:
            raise HTTPException(status_code=400, detail="User not found")
        
        # Save message
        await conn.execute("""
            INSERT INTO messages (username, message, tg_user_id, timestamp)
            VALUES ($1, $2, $3, $4)
        """, message.username, message.message, message.tg_user_id, datetime.utcnow())
        
        return {"msg": "Message saved"}
    finally:
        await conn.close()
        raise HTTPException(status_code=400, detail="User not found")
    
    # Save message to database
    messages.insert().values(
        username=message.username,
        message=message.message,
        tg_user_id=message.tg_user_id,
        timestamp=datetime.utcnow()
    )
    await database.execute(query)
    return {"msg": "Message saved"}