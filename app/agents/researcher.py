from agents import Agent, Runner, Trace
from dotenv import load_dotenv
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field

import httpx

from app.config import settings
from app.context import AppContext
# from app.tools.serper_search_tool import web_search

load_dotenv(override=True)


class ResearchSource(BaseModel):
    title: str = Field(
        description="Title of the source."
    )

    url: str = Field(
        description="URL of the source."
    )


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

    sources: list[ResearchSource] = Field(
        description="Sources used to support the research findings."
    )

    conclusion: str = Field(
        description="A concise conclusion synthesizing the main findings."
    )


research_agent = Agent(
    name="Senior Researcher Agent",
    instructions=open("app/prompts/researcher.md").read(),
    model=settings.model,
    output_type=ResearchResult,
)


async def run_research_agent(user_query: str, search_results: list[str]):
    """ Invoke the agent with the user_query and the search_results """

    try:

        researcher_prompt = f"""
            User Query: 
            {user_query}

            Search Results:
            {search_results}
        """
        
        research_result = await Runner.run(research_agent, researcher_prompt)

        return research_result.final_output

    except Exception as e:
        print(f"invoking researcher agent failed: {e}")
        return f"invoking researcher agent failed: {e}"



if __name__ == "__main__":

    searched_results = """
        Introducing the Agents API https://openai.com/index/introducing-the-agents-api/
        Top 5 LLM and Agent Observability Tools in 2026 https://mlflow.org/top-5-agent-observability-tools/
        NVIDIA Launches Open Agent Safety Platform to Secure ... https://nvidianews.nvidia.com/news/open-agent-safety-platform
        LangChain Blog https://www.langchain.com/blog
        Intent: research
        Output: ["Introducing the Agents API\nhttps://openai.com/index/introducing-the-agents-api/\nOpenAI's Agents API enables us to build more reliable agents, giving customers the confidence to use them in production. By separating the agent ...", 'LangChain Blog\nhttps://www.langchain.com/blog\nSeptember 25, 2026. 9. min ... LangSmith, our agent engineering platform, helps developers debug every agent decision, eval changes, and deploy in one click.', 'Top 5 LLM and Agent Observability Tools in 2026\nhttps://mlflow.org/top-5-agent-observability-tools/\nAgent observability is end-to-end visibility into every step an AI agent takes in production: LLM calls, tool invocations, retrieval steps, planning decisions, ...', 'NVIDIA Launches Open Agent Safety Platform to Secure ...\nhttps://nvidianews.nvidia.com/news/open-agent-safety-platform\nNVIDIA today announced NVIDIA Open Agent Safety Platform, an open software platform and reference system design to strengthen AI security ...']
    """

    print('testing research agent...')
    result = asyncio.run(run_research_agent("Research the latest developments in AI agents in 2026, including major framework updates and production trends.", searched_results))
    print(result)