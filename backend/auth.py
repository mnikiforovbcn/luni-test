from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import users, database
from passlib.hash import bcrypt

router = APIRouter()

class UserIn(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserIn):
    query = users.select().where(users.c.username == user.username)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Username taken")
    hashed = bcrypt.hash(user.password)
    query = users.insert().values(username=user.username, password=hashed)
    await database.execute(query)
    return {"msg": "Registered"}

@router.post("/login")
async def login(user: UserIn):
    query = users.select().where(users.c.username == user.username)
    db_user = await database.fetch_one(query)
    if not db_user or not bcrypt.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"msg": "Logged in"}