#app/memory/schemas.py

from pydantic import BaseModel


class ResearchMemory(BaseModel):
    topic: str
    content: str
    source_url: str | None = None
