from fastapi.routing import APIRouter
api_router = APIRouter()
from starlette.responses import StreamingResponse
from finbot_platform.web.api.agent.streaming_services import OpenAIStreaming
from finbot_platform.schemas.agent import StreamingRequest
from finbot_platform.schemas.agent import MessageRequest
from finbot_platform.db.sql_connection import Connection
from finbot_platform.settings import settings
from .vector_util import VectorSupport
import time
router = APIRouter()
streamClient = OpenAIStreaming()
vdb = VectorSupport()
@router.get(
    "/test")
async def test():
    return "Hello"
@router.post(
    "/openai_streaming",
)

async def openai_streaming(request: StreamingRequest) -> StreamingResponse:
    print(request.message)
    return StreamingResponse(streamClient.stream_generator(await streamClient.streamNow(request.message)),
                             media_type='text/event-stream')


@router.post(
    "/run",
)

async def agents_run(request: MessageRequest) -> StreamingResponse:
    # print(request.message)
    query_metadata: dict | None = vdb.query_vector(request.query)
    if query_metadata:
        if query_metadata["query_type"] == 'account_info' and query_metadata["agent_type"] == "sql_agent":
            start_time = time.time()
            sql_query = query_metadata["query_info"] + str(request.userId)
            print(f"INFO: SQL QUERY GENERATED: {sql_query}")
            with Connection(settings.db_config) as db:
                result = db.fetch(sql_query)
                print(query_metadata['answer_template'])
                final_answer = query_metadata['answer_template'].format(result=result)
                end_time = time.time()
                print(f"Time taken for running sql chain: {end_time - start_time}")
                return StreamingResponse(streamClient.stream_string(final_answer),
                                         media_type='text/event-stream')
                # print(f"Found the answer: {final_answer}")
            # FQ.sql_query(user_dict)
    else:
        print(f"INFO: ANOTHER AGENT IS RUNNING TO PROCESS YOUR REQUEST....")
        return StreamingResponse(streamClient.stream_generator(await streamClient.streamNow(request.query)),
                                 media_type='text/event-stream')