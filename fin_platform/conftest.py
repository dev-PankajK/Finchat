import pytest
# from dotenv import load_dotenv
# load_dotenv(override=True)
from finbot_platform.db.connection import Connection
from finbot_platform.settings import settings
from finbot_platform.db.models.user import User
from sqlmodel import SQLModel
from sqlalchemy import create_engine

@pytest.fixture(scope="session")
def _engine():
    """
    Create engine and databases.

    :yield: new engine.
    """
    from finbot_platform.db.models import load_all_models
    engine = create_engine(settings.db_url, echo=True)
    # Now check the user table existance and if there is no table than create all tables in the database
    with Connection(settings.db_url) as db:
        with engine.connect() as connection:
            if not engine.dialect.has_table(connection, User.__table__.name):
                print(f"INFO: User table does not exist creating all the tables.....")
                load_all_models()
                SQLModel.metadata.create_all(db.engine)
                print(f"INFO: Successfully created all the tables.")
                connection.close()
            else:
                print(f"INFO:Database with all the tables already exists.Skipping...")
    try:
        yield {
            "test": "ok"
        }
    finally:
        engine.dispose()
