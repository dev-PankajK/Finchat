from finbot_platform.schemas.auth import RequestLogin,CreateUserRequest
from finbot_platform.db.connection import Connection
from finbot_platform.db.models.user import User
from finbot_platform.web.api.auth.login_utils import get_password_hash
from finbot_platform.settings import settings


def create_user(user:CreateUserRequest):
    user = User(
        username = user.username,
        hashed_password = get_password_hash(user.password)
    )
    with Connection(settings.db_url) as db:
        created_user = db.insert(user)
        print(f"This is created user: {created_user} and type : {type(created_user)}")
    return created_user