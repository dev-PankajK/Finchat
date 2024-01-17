from finbot_platform.db.crud.user import create_user
from finbot_platform.schemas.auth import CreateUserRequest
from finbot_platform.db.models.user import User



test_user = {
    "username": "abc.cdf@gmail.com",
    "password": "test123"
}

def test_create_a_user(_engine):
    assert _engine["test"] == "ok"
    create_test_user = CreateUserRequest(**test_user)
    user = create_user(create_test_user)
    assert isinstance(user,User)
    assert user.username == create_test_user.username