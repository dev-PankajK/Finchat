from openai import AsyncOpenAI
import async_timeout
import asyncio
from finbot_platform.settings import settings
from fastapi import HTTPException
import openai
from openai.types.chat import ChatCompletionChunk
from openai._streaming import AsyncStream

class OpenAIStreaming():
    def __init__(self,GENERATION_TIMEOUT_SEC=60):
        self.GENERATION_TIMEOUT_SEC = GENERATION_TIMEOUT_SEC
        self.asyncClient = AsyncOpenAI(api_key=settings.openai_api_key)

    async def stream_generator(self,subscription):
        async with async_timeout.timeout(self.GENERATION_TIMEOUT_SEC):
            try:
                async for chunk in subscription:
                    yield "data: " + (chunk.choices[0].delta.content or "") + "\n\n"

            except asyncio.TimeoutError:
                raise HTTPException(status_code=504, detail="Stream timed out")

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
