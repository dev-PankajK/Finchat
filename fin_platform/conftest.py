import pytest
# from dotenv import load_dotenv
# load_dotenv(override=True)
from finbot_platform.db.connection import Connection
from finbot_platform.settings import settings
from finbot_platform.db.models.user import User
from sqlmodel import SQLModel
from sqlalchemy import create_engine
is_table_exist = False
@pytest.fixture(scope="session")
def _engine():
    """
    Create engine and databases.

    :yield: new engine.
    """
    from finbot_platform.db.models import load_all_models
    engine = create_engine(settings.db_url, echo=True)
    with engine.connect() as connection:
        if engine.dialect.has_table(connection, User.__table__.name):
            global is_table_exist
            is_table_exist = True
            connection.close()
    if not is_table_exist:
        with Connection(settings.db_url) as db:
            print(f"INFO: User table does not exist creating all the tables.....")
            load_all_models()
            SQLModel.metadata.create_all(db.engine)
            print(f"INFO: Successfully created all the tables.")
    # Now check the user table existance and if there is no table than create all tables in the database
    try:
        yield {
            "test": "ok"
        }
    finally:
        engine.dispose()
