from agents import Agent, Runner, Trace
from dotenv import load_dotenv
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field

import httpx

from app.config import settings
from app.context import AppContext
from app.tools.serper_search_tool import web_search

load_dotenv(override=True)


class ResearchResult(BaseModel):
    topic: str = Field(
        description="The main topic or research question investigated."
    )

    summary: str = Field(
        description="A concise overview of the research findings."
    )

    key_findings: list[str] = Field(
        description="The most important factual findings discovered during the research."
    )

    sources: list[str] = Field(
        description="A list of URLs or references used to support the research findings."
    )

    conclusion: str = Field(
        description="A concise conclusion that synthesizes the main findings of the research."
    )

research_agent = Agent(
    name="Researcher Agent",
    instructions=open("app/prompts/researcher.md").read(),
    model=settings.model,
    tools=[web_search],
    output_type=ResearchResult,
)


if __name__ == "__main__":

    # task = "Compare Next.js App Router vs Pages Router: what are the main differences and which should a new project use in 2026?"
    task = "Tell me about latest tech news 2026"

    async def main():
        async with httpx.AsyncClient(timeout=20) as http:
            ctx = AppContext(user_id="test", http=http)
            result = await Runner.run(research_agent, task, context=ctx)
            print(result.final_output)

    asyncio.run(main())