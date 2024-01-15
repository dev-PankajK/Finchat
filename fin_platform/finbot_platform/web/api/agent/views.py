from fastapi.routing import APIRouter
from starlette.responses import StreamingResponse
from finbot_platform.web.api.agent.streaming_services import OpenAIStreaming
from finbot_platform.schemas.agent import StreamingRequest
from finbot_platform.db.models.user import User
from finbot_platform.db.sql_connection import Connection
from finbot_platform.settings import settings
from .vector_util import VectorSupport
from fastapi import Depends,Request,Body
from typing import Annotated
from finbot_platform.web.api.agent.dependencies import get_user_message,get_current_user
from finbot_platform.web.api.agent.llm_agents import lang_multitool_agent
import time
router = APIRouter()
streamClient = OpenAIStreaming()
vdb = VectorSupport()
LANG_AGENT = lang_multitool_agent(1)
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
async def agents_run(current_user: Annotated[User, Depends(get_current_user)],userMessage: str = Depends(get_user_message)) -> StreamingResponse:
    # print(request.message)
    query_metadata: dict | None = vdb.query_vector(userMessage)
    if query_metadata:
        if query_metadata["query_type"] == 'account_info' and query_metadata["agent_type"] == "sql_agent":
            start_time = time.time()
            sql_query = query_metadata["query_info"] + str(current_user.id)
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
        # return StreamingResponse(streamClient.stream_generator(await streamClient.streamNow(request.query)),
        #                          media_type='text/event-stream')
        return StreamingResponse(streamClient.stream_string("Currently I can't answer this question! Sorry..."),
                                 media_type='text/event-stream')



@router.post(
    "/lang_multiool_agent",
)
async def langMultiToolAgent(userMessage:StreamingRequest) -> StreamingResponse:
    response = LANG_AGENT.invoke({"input": userMessage})
    return StreamingResponse(streamClient.stream_string(response['output']),
                                 media_type='text/event-stream')