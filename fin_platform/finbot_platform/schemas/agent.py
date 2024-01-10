from pydantic import BaseModel



class StreamingRequest(BaseModel):
    message: str

class AgentRun(BaseModel):
    query: str
    access_token: str #TODO CHANGE IT

