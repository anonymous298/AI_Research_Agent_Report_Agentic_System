import datetime
from typing import Literal
# from agents import Agent, Runner, Trace
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field

from app.config import settings
# from app.context import AppContext
# from app.tools.serper_search_tool import web_search

load_dotenv(override=True)


# Structure Output For planner Agent
class PlannerStructuredOutput(BaseModel):
    intent: Literal["conversation", "research"]
    search_queries: list[str] = Field(default_factory=list)


# Planner Agent  # Using Normal LLM OpenAI SDK Instead For Simple Planning
# planner_agent = Agent(
#     name="Planner Agent",
#     instructions=open("app/prompts/planner.md").read(),
#     model=settings.model,
#     output_type=PlannerStructuredOutput,
# )


# OpenAI LLM SDK
client = AsyncOpenAI()


# Function for executing our LLM Call to generate a Structured Output for the Pipeline
async def plan(task: str) -> PlannerStructuredOutput:
    """ Executes our planner LLM call and returns Planner Structured Output """

    planner_prompt = Path("app/prompts/planner.md").read_text()

    planner_prompt = planner_prompt.replace(
        "{current_date}",
        datetime.datetime.now().strftime("%Y-%m-%d")
    )

    response = await client.responses.parse(
        model=settings.model,
        instructions=planner_prompt,
        input=task,
        text_format=PlannerStructuredOutput,

    )

    return response.output_parsed


# For single file testing
if __name__ == "__main__":

    # Executes the Agent Loop not required yet
    # task = "Research the latest OpenAI Agents SDK features, architecture, and best practices for building production agentic systems."
    task = "What’s the difference between async and sync programming in Python?"

    # print("Planner Agent Testing Runs...")
    # result = asyncio.run(Runner.run(planner_agent, task))

    # print(result.final_output)

    
    # Testing our LLM SDK call 

    print("Testing Planner LLM SDK call")
    response = asyncio.run(plan(task))
    print(response)