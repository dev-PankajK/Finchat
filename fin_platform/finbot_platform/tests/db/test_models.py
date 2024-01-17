from finbot_platform.db.crud.user import create_user
from finbot_platform.schemas.auth import CreateUserRequest
from finbot_platform.db.models.user import User


from finbot_platform.db.models import load_all_models
from finbot_platform.db.connection import Connection
from finbot_platform.settings import settings
from finbot_platform.db.models.user import User
from sqlmodel import SQLModel
from sqlalchemy import create_engine
engine = create_engine(settings.db_url, echo=True)
#Now check the user table existance and if there is no table than create all tables in the database
with Connection(settings.db_url) as db:
    with engine.connect() as connection:
        if not engine.dialect.has_table(connection,User.__table__.name):
            print(f"INFO: User table does not exist creating all the tables.....")
            load_all_models()
            SQLModel.metadata.create_all(db.engine)
            print(f"INFO: Successfully created all the tables.")
            connection.close()
        else:
            print(f"INFO:Database with all the tables already exists.Skipping...")

test_user = {
    "username": "abc.cdf@gmail.com",
    "password": "test123"
}

def test_create_a_user():
    create_test_user = CreateUserRequest(**test_user)
    user = create_user(create_test_user)
    assert isinstance(user,User)
    assert user.username == create_test_user.username
