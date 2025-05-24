import databases
import sqlalchemy
import logging
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://luni:luni@luni-db-mkhailluni.db-msk0.amvera.tech:5432/luni_db?sslmode=require"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
)

try:
    engine = sqlalchemy.create_engine(DATABASE_URL)
    metadata.create_all(engine)
    logger.info("Successfully connected to the database and created tables")
except SQLAlchemyError as e:
    logger.error(f"Error connecting to database: {e}")
    raise

async def init_db():
    try:
        await database.connect()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise