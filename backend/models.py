import sqlalchemy
from db import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("age", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("gender", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("tg_user_id", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("tg_username", sqlalchemy.String, nullable=True)
)

messages = sqlalchemy.Table(
    "messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("message", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("tg_user_id", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime, nullable=False)
)