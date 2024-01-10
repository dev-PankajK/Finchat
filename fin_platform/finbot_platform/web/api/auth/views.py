from fastapi.routing import APIRouter
from fastapi import  HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from finbot_platform.schemas.auth import RequestLogin,CreateUserRequest
from .login_utils import get_password_hash,verify_password,create_jwt_access_token
from finbot_platform.db.models.user import User
from finbot_platform.db.connection import Connection
from finbot_platform.settings import settings
router = APIRouter()
from sqlmodel import select
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "testuser@gmail.com": {
        "username": "testuser@gmail.com",
        "password": "testpassword",
    }
}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get(
    "/test")

@router.post(
    "/sineup",
)
async def userSignup(request: CreateUserRequest):
    print(f"Getting user Details")
    print(request.username, request.password)
    user = User(
        username = request.username,
        hashed_password = get_password_hash(request.password)
    )
    with Connection(settings.db_url) as db:
        created_user = db.insert(user)
        print(created_user)
    return created_user


async def test():
    return "Hello"
@router.post(
    "/login",
)
async def userLogin(request: RequestLogin):
    print(f"Getting user Details")
    print(request.username, request.password)
    with Connection(settings.db_url) as db:
        sql_st = select(User).where(User.username == request.username)
        user = db.fetch(sql_st).first()
    if user is None or not verify_password(request.password,user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_jwt_access_token({"id": user.id})
    return {"access_token": access_token, "token_type": "bearer","success": True}


