import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings # Assuming settings.DATABASE_URL is defined here

# Define the SQLAlchemy declarative base
Base = declarative_base()

# Create the asynchronous engine
# Use settings.DATABASE_URL from your config
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True, # Set to False in production for less logging
    future=True
)

# Create a sessionmaker to create AsyncSession objects
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False # This prevents attributes from expiring after commit
)


async def get_db_session():
    """
    Dependency to get an asynchronous database session.
    It yields a session and ensures it's closed after use.
    """
    async with AsyncSessionLocal() as session:
        yield session

# --- IMPORTANT: Ensure settings.DATABASE_URL is set in your .env ---
# For PostgreSQL: DATABASE_URL="postgresql+asyncpg://user:password@host:port/dbname"
# For SQLite:     DATABASE_URL="sqlite+aiosqlite:///./faber.db" (adjust path as needed)
# You will need to install 'aiosqlite' for SQLite: pip install aiosqlite
