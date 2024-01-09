from fastapi.routing import APIRouter

from finbot_platform.web.api import agent,auth

api_router = APIRouter()

api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
