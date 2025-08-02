import os
import asyncpg
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Numeric,
    BigInteger,
    ForeignKey,
    DateTime,
    JSON,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("telegram_id", BigInteger, primary_key=True),
    Column("username", String),
    Column("balance", Numeric(10, 2), default=0.0),
    Column("created_at", DateTime, default=datetime.utcnow),
)

games = Table(
    "games",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("creator_id", BigInteger, ForeignKey("users.telegram_id")),
    Column("opponent_id", BigInteger, ForeignKey("users.telegram_id"), nullable=True),
    Column("stake", Numeric(10, 2)),
    Column("pot", Numeric(10, 2)),
    Column("win_condition", Integer),  # 1, 2, or 4 tokens
    Column("board_state", JSON),
    Column("current_turn_id", BigInteger, nullable=True),
    Column("last_action_timestamp", DateTime, nullable=True),
    Column("status", String, default="lobby"),  # lobby, active, finished, forfeited
    Column("winner_id", BigInteger, ForeignKey("users.telegram_id"), nullable=True),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
)

transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", BigInteger, ForeignKey("users.telegram_id")),
    Column("amount", Numeric(10, 2)),
    Column("type", String),  # deposit, withdrawal, stake, prize
    Column("status", String),  # pending, completed, failed
    Column("chapa_tx_ref", String, nullable=True, unique=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)

async def get_db_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())