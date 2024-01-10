
from settings import settings
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
engine = create_engine(settings.db_url)
import asyncio
try:
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE {settings.db_url};"))
except Exception as e:
    print(f"INFO: DATABASE DOES NOT EXIST.")

async def create_database() -> None:
    """Create a database."""
    engine = create_async_engine(settings.db_url)
    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(text(f"CREATE DATABASE {settings.db_base};"))

async def main():
    await create_database()
if __name__ == "__main__":
    # Create an event loop and run the main function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()


