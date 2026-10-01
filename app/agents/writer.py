from agents import Agent, Runner, Trace
from dotenv import load_dotenv
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field

from app.agents.researcher import ResearchSource
from app.config import settings

load_dotenv(override=True)

# Sturctured output 
class WriterFinalResponse(BaseModel):
    answer: str
    sources: list[ResearchSource]

# writer agent
writer_agent = Agent(
    name="Senior Writer Agent",
    instructions=open("app/prompts/writer.md").read(),
    model=settings.model,
    output_type=WriterFinalResponse,
)

# agent invoking function
async def run_writer(user_query: str, researched_results):
    """ Exeuctes the writer agent """

    try: 

        writer_prompt = f"""
            User Query:
            {user_query}

            Research Result:
            {researched_results.model_dump_json()}
        """

        writer_response = await Runner.run(writer_agent, writer_prompt)

        return writer_response.final_output

    except Exception as e:
        print(f"writer agent block failed: {e}")
        return f"writer agent block failed: {e}"


