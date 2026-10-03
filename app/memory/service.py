from sqlalchemy.ext.asyncio import AsyncSession

from app.memory.embeddings import create_embedding
from app.memory.repository import MemoryRepository
from app.memory.schemas import ResearchMemory


class MemoryService:

    # Initializing Constructor
    def __init__(self):
        self.repository = MemoryRepository()

    # memory saving method
    async def save_memory(
        self,
        session: AsyncSession,
        memory: ResearchMemory
    ):

        # creating embeddings of query
        embedding = await create_embedding(memory.content)

        return await self.repository.save(
            session, 
            memory, 
            embedding
        )

    # retrieving recent memories method
    async def get_recent_memories(
        self, 
        session: AsyncSession,
        limit: int = 5,
    ):

        return await self.repository.get_recent(session, limit)

    async def retrieve_similar_searches(
        self, 
        session: AsyncSession,
        text: str,
        limit: int = 5,
    ):
        """ Retrieve similar searches using embedding of input text """

        embedding = await create_embedding(text)

        return await self.repository.search_similar(session, embedding, limit)
    
