from pydantic import BaseModel



class StreamingRequest(BaseModel):
    message: str

