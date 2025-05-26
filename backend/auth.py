from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db import users, database
from passlib.hash import bcrypt

router = APIRouter()

class UserIn(BaseModel):
    tg_user_id: str
    username: str | None = None
    age: int | None = None
    gender: str | None = None
    tg_username: str | None = None

@router.post("/register")
async def register(user: UserIn):
    query = users.select().where(users.c.username == user.username)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Username taken")
    query = users.insert().values(
        username=user.username,
        age=user.age,
        gender=user.gender,
        tg_user_id=user.tg_user_id,
        tg_username=user.tg_username
    )
    await database.execute(query)
    return {"msg": "Registered"}

@router.post("/check_user")
async def check_user(tg_user_id: str):
    query = users.select().where(users.c.tg_user_id == tg_user_id)
    db_user = await database.fetch_one(query)
    if db_user:
        return {"exists": True, "username": db_user.username}
    return {"exists": False}

@router.post("/login")
async def login(user: UserIn):
    query = users.select().where(users.c.tg_user_id == user.tg_user_id)
    db_user = await database.fetch_one(query)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Update user info if any fields were provided
    update_data = {}
    if user.username is not None:
        update_data[users.c.username] = user.username
    if user.age is not None:
        update_data[users.c.age] = user.age
    if user.gender is not None:
        update_data[users.c.gender] = user.gender
    if user.tg_username is not None:
        update_data[users.c.tg_username] = user.tg_username
    
    if update_data:
        update_query = users.update().where(users.c.tg_user_id == user.tg_user_id).values(update_data)
        await database.execute(update_query)
    return {"msg": "Logged in", "username": db_user.username}