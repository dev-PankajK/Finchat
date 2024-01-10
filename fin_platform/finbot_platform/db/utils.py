from sqlmodel import create_engine, SQLModel
from finbot_platform.settings import settings




def create_dbengine():
    """
    Creates SQLModel engine instance.

    :return: SQLModel engine instance.
    """

    if settings.environment == "development":
        return create_engine(
            settings.db_url,
            echo=settings.db_echo,
        )


    return create_engine(
        settings.db_url,
        echo=settings.db_echo,
    )

def check_db_existance():
    from sqlalchemy import create_engine
    from sqlalchemy.exc import ProgrammingError
    engine = create_engine(settings.db_url)
    try:
        with engine.connect() as connection:
            return True
    except ProgrammingError as e:
        print(f"INFO: DATABASE DOES NOT EXIST.")
        return False

def create_database():
    #TODO: Currently not able to create database using this, need to be implement in future
    from sqlalchemy import create_engine,text
    engine = create_engine(settings.db_url)
    try:
        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE {settings.db_url};"))
    except Exception as e:
        print(f"INFO: DATABASE DOES NOT EXIST.")
        return False
def create_tables() -> None:
    """Create Table in your db."""
    #TODO: drop the data if exists also implement asyncConnection
    from finbot_platform.db.models import load_all_models
    load_all_models()
    print("All models loaded")
    SQLModel.metadata.create_all(create_dbengine())


if __name__ == "__main__":
    create_tables()