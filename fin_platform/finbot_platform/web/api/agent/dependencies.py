from finbot_platform.schemas.agent import AgentRun
from fastapi import Body
from typing import Annotated
from fastapi import Depends,HTTPException,status
from finbot_platform.db.connection import Connection
from sqlmodel import select
from finbot_platform.db.models.user import User
from finbot_platform.settings import settings
from jose import JWTError, jwt

async def get_user_message(body:AgentRun= Body()) -> str:
    return body.query


async def get_current_user(body:AgentRun=Body()):
    #TODO: Move this method to somewhere else to optimise
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(body.access_token, settings.JWT_SECRET_KEY, algorithms="HS256")
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    with Connection(settings.db_url) as db:
        sql_st = select(User).where(User.id == user_id)
        user = db.fetch(sql_st).first()
    if user is None:
        raise credentials_exception
    return user