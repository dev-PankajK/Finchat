from fastapi.routing import APIRouter
from fastapi import  HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from finbot_platform.schemas.auth import RequestLogin,CreateUserRequest
from .login_utils import get_password_hash
from finbot_platform.db.models.user import User
from finbot_platform.db.connection import Connection
from finbot_platform.settings import settings
router = APIRouter()

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
    user = fake_users_db.get(request.username)
    if user is None or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": request.username, "token_type": "bearer"}


