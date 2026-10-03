from sqlalchemy.ext.asyncio import AsyncSession

from app.memory.models import ResearchMemoryModel
from app.memory.schemas import ResearchMemory
from sqlalchemy import select


class MemoryRepository:

    async def save(
        self,
        session: AsyncSession,
        memory: ResearchMemory,
        embedding: list[float],
    ) -> ResearchMemoryModel:
        
        ''' Saving memory data in database '''

        try:

            db_memory = ResearchMemoryModel(
                topic=memory.topic,
                content=memory.content,
                source_url=memory.source_url,
                embedding=embedding,
            )

            session.add(db_memory)

            await session.commit()
            await session.refresh(db_memory)
            # await session.close()

            return db_memory

        except Exception as e:
            print(f"save data repository function not working: {e}")
            return f"save data repository function not working: {e}"

    async def get_recent(
        self,
        session: AsyncSession,
        limit: int = 5,
    ) -> list[ResearchMemoryModel]:

        """ get recent data """

        try:
                
            result = await session.execute(
                select(ResearchMemoryModel)
                .order_by(ResearchMemoryModel.created_at.desc())
                .limit(limit)
            )

            return list(result.scalars().all())

        except Exception as e:
            print(f"recent data repo function not working: {e}")
            return []


    async def search_similar(
        self,
        session: AsyncSession,
        embedding: list[float],
        limit: int = 5,
    ):
        """ Get similar data using cosine similarity of input embedding """

        try:

            result = await session.execute(
                select(ResearchMemoryModel)
                .order_by(
                    ResearchMemoryModel.embedding.cosine_distance(embedding)
                )
                .limit(limit)
            )

            return list(result.scalars().all())

        except Exception as e:
            print(f'similarity search data error: {e}')
            return []
