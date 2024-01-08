from pydantic import BaseModel



class StreamingRequest(BaseModel):
    message: str

class MessageRequest(BaseModel):
    query: str
    userId: int #TODO CHANGE IT

