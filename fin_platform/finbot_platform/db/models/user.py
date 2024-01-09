from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "testUser"
    id: int = Field(default=None, primary_key=True)
    username: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    email_verified: datetime = Field(nullable=True, alias="emailVerified")
    create_date: datetime = datetime.now()