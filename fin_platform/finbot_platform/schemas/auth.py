from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str


class RequestLogin(BaseModel):
    username: str
    password: str
class MessageRequest(BaseModel):
    query: str
    userId: int #TODO CHANGE IT

class AuthToken(BaseModel):
    access_token: str
    token_type: str
