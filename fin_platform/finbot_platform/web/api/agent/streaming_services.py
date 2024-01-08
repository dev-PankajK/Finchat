from openai import AsyncOpenAI
import async_timeout
import asyncio
from finbot_platform.settings import settings
from fastapi import HTTPException
import openai
from openai.types.chat import ChatCompletionChunk
from openai._streaming import AsyncStream
from typing import AsyncGenerator
import tiktoken
class OpenAIStreaming():
    def __init__(self,GENERATION_TIMEOUT_SEC=60):
        self.GENERATION_TIMEOUT_SEC = GENERATION_TIMEOUT_SEC
        self.asyncClient = AsyncOpenAI(api_key=settings.openai_api_key)

    async def stream_generator(self,subscription): #TODO: change here
        async with async_timeout.timeout(self.GENERATION_TIMEOUT_SEC):
            try:
                async for chunk in subscription:
                    yield "data: " + (chunk.choices[0].delta.content or "") + "\n\n"

            except asyncio.TimeoutError:
                raise HTTPException(status_code=504, detail="Stream timed out")

    async def string_stream_generator(self,data: str, delayed: bool) -> AsyncGenerator[bytes, None]:
        if delayed:
            encoding = tiktoken.get_encoding("cl100k_base")
            token_data = encoding.encode(data)
            for token in token_data:
                print(encoding.decode([token]))
                chunk = "data: " + (encoding.decode([token])) + "\n\n"
                yield chunk
                await asyncio.sleep(0.25)  # simulate slow processing
        else:
            yield data.encode()

    async def streamNow(self,prompt,history=()) -> AsyncStream[ChatCompletionChunk]:
        try:
            stream = await self.asyncClient.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}], #TODO: implement history
                stream=True,
            )
            return stream
        except openai.OpenAIError as e: #TODO: handle OPENAI error separately
            print(e)
            raise HTTPException(status_code=500, detail='OpenAI call failed')


    def stream_string(self,data: str, delayed: bool = True):
        return self.string_stream_generator(data,delayed)
