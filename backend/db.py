import databases
import sqlalchemy
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://luni:luni@localhost:5432/luni"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, server_default=sqlalchemy.text("nextval('users_id_seq'::regclass)")),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("age", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("gender", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("tg_user_id", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("tg_username", sqlalchemy.String, nullable=True)
)

async_engine = create_async_engine(
    DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True
)

async def init_db():
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata.create_all)
            logger.info("Database tables created successfully")
        await database.connect()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise