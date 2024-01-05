from fastapi.routing import APIRouter

from finbot_platform.web.api import agent

api_router = APIRouter()

api_router.include_router(agent.router, prefix="/agent", tags=["agent"])

