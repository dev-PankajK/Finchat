from fastapi.routing import APIRouter
api_router = APIRouter()
from starlette.responses import StreamingResponse
from finbot_platform.web.api.agent.streaming_services import OpenAIStreaming
from finbot_platform.schemas.agent import StreamingRequest

router = APIRouter()
@router.get(
    "/test")
async def test():
    return "Hello"
@router.post(
    "/openai_streaming",
)

async def openai_streaming(request: StreamingRequest) -> StreamingResponse:
    print(request.message)
    streamClient = OpenAIStreaming()
    return StreamingResponse(streamClient.stream_generator(await streamClient.streamNow(request.message)),
                             media_type='text/event-stream')
