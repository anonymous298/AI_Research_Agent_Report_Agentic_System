import asyncio
from openai import AsyncOpenAI

from app.config import settings


# creating embedding model openai client
client = AsyncOpenAI(api_key=settings.openai_api_key)


async def create_embedding(text: str) -> list[float]:
    """ Take text input and returns embedding vector list """

    response = await client.embeddings.create(
        model=settings.embedding_model,
        input=text
    )

    return response.data[0].embedding



#testing
if __name__ == "__main__":
    async def main():
        text = 'Agentic AI has so much potential to scale'

        embedding = await create_embedding(text)

        print("Embedding: ", len(embedding))

    asyncio.run(main())