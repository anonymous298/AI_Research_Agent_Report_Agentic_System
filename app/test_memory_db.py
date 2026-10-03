import asyncio
import selectors

from app.config import settings
from app.core.database import AsyncSessionLocal, init_db
# from app.memory.repository import MemoryRepository
from app.memory.schemas import ResearchMemory
from app.memory.service import MemoryService

# print(settings.database_url)

async def main():
    await init_db()
    print("Database initialized successfully!")

    memory = ResearchMemory(
        topic="Ancient History",
        content="Ancient civilizations developed systems of writing, government, trade, architecture, and mathematics that influenced later societies.",
        source_url="https://example.com/ancient-history",
    )

    memory_service = MemoryService()

    async with AsyncSessionLocal() as session:
        # saved_memory = await memory_service.save_memory(session, memory)

        # print("Memory saved!")
        # print("ID:", saved_memory.id)
        # print("Topic:", saved_memory.topic)
        # print("Content:", saved_memory.content)
        # print("Created_At:", saved_memory.created_at)

        # recent_memory = await memory_service.get_recent_memories(session)

        # for memory in recent_memory:
        #     print("Content:", memory.content)

        similar_memory = await memory_service.retrieve_similar_searches(session, "what is ai?")

        for memory in similar_memory:
            print("Content: ", memory.content)

        print(len(similar_memory))

        

if __name__ == "__main__":
    asyncio.run(main(), loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()),)